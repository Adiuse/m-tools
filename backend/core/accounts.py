import hashlib
import json
from datetime import timedelta
from smtplib import SMTPException

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

from .models import AuthThrottle, User


AUTH_WINDOW = timedelta(minutes=10)


def csrf_failure(request, reason=""):
    return JsonResponse({"code": "csrf_failed"}, status=403)


@ensure_csrf_cookie
@require_GET
def session(request):
    user = request.user
    return JsonResponse({
        "user": {"id": user.pk, "email": user.email} if user.is_authenticated else None,
    })


def allowed(action, address):
    key = hashlib.sha256(f"{action}:{address}".encode()).hexdigest()
    now = timezone.now()
    with transaction.atomic():
        AuthThrottle.objects.filter(window_end__lte=now).delete()
        bucket, created = AuthThrottle.objects.select_for_update().get_or_create(
            key=key, defaults={"window_end": now + AUTH_WINDOW},
        )
        if created:
            return True
        if bucket.count >= 50:
            return False
        bucket.count += 1
        bucket.save(update_fields=["count"])
    return True


def payload(request, action):
    if not allowed(action, request.META.get("REMOTE_ADDR", "")):
        return None, JsonResponse({"code": "rate_limited"}, status=429)
    try:
        data = json.loads(request.body)
    except (UnicodeDecodeError, ValueError):
        return None, JsonResponse({"code": "bad_json"}, status=400)
    if not isinstance(data, dict):
        return None, JsonResponse({"code": "invalid_input"}, status=422)
    return data, None


def email_from(data):
    email = data.get("email")
    if not isinstance(email, str) or len(email) > 254:
        raise ValidationError("Invalid email.")
    email = email.strip().lower()
    validate_email(email)
    return email


def send_link(user, mode):
    token = default_token_generator.make_token(user)
    link = f"{settings.PUBLIC_ORIGIN.rstrip('/')}/#mode={mode}&uid={user.pk}&token={token}"
    try:
        send_mail("M-Tools · Account", link, settings.DEFAULT_FROM_EMAIL, [user.email])
    except (SMTPException, OSError):
        # The response is the same for registered and unknown addresses.
        return


@require_POST
@csrf_protect
def sign_in(request):
    data, error = payload(request, "login")
    if error is not None:
        return error
    raw_email = data.get("email")
    password = data.get("password")
    if not isinstance(raw_email, str) or not isinstance(password, str) or len(password) > 4096:
        return JsonResponse({"code": "invalid_input"}, status=422)
    user = authenticate(request, email=raw_email.strip().lower(), password=password)
    if user is None:
        return JsonResponse({"code": "invalid_credentials"}, status=401)
    login(request, user)
    return JsonResponse({"user": {"id": user.pk, "email": user.email}})


@require_POST
@csrf_protect
def sign_out(request):
    logout(request)
    return JsonResponse({"user": None})


@require_POST
@csrf_protect
def register(request):
    data, error = payload(request, "register")
    if error is not None:
        return error
    try:
        email = email_from(data)
    except ValidationError:
        return JsonResponse({"code": "invalid_email"}, status=422)
    user, _ = User.objects.get_or_create(email=email, defaults={"is_active": False, "password": "!"})
    if not user.is_active and not user.has_usable_password():
        send_link(user, "activate")
    return JsonResponse({"status": "accepted"}, status=202)


@require_POST
@csrf_protect
def request_reset(request):
    data, error = payload(request, "request-reset")
    if error is not None:
        return error
    try:
        email = email_from(data)
    except ValidationError:
        return JsonResponse({"code": "invalid_email"}, status=422)
    user = User.objects.filter(email=email, is_active=True).first()
    if user is not None and user.has_usable_password():
        send_link(user, "reset")
    return JsonResponse({"status": "accepted"}, status=202)


@require_POST
@csrf_protect
@transaction.atomic
def set_password(request):
    data, error = payload(request, "set-password")
    if error is not None:
        return error
    mode, uid, token, password = (data.get(key) for key in ("mode", "uid", "token", "password"))
    if mode not in ("reset", "activate") or not all(isinstance(item, str) for item in (uid, token, password)):
        return JsonResponse({"code": "invalid_input"}, status=422)
    if len(uid) > 36 or len(token) > 100 or len(password) > 4096:
        return JsonResponse({"code": "invalid_input"}, status=422)
    try:
        user = User.objects.select_for_update().filter(pk=uid, is_active=(mode == "reset")).first()
    except ValidationError:
        user = None
    if user is None or not default_token_generator.check_token(user, token):
        return JsonResponse({"code": "invalid_link"}, status=422)
    try:
        validate_password(password, user)
    except ValidationError as exc:
        return JsonResponse({"code": "weak_password", "fields": {"password": exc.messages}}, status=422)
    user.set_password(password)
    user.is_active = True
    user.save(update_fields=["password", "is_active"])
    return JsonResponse({"status": "saved"})
