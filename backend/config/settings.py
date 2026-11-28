import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

ROOT = Path(__file__).resolve().parents[2]
DEBUG = os.environ.get("MTOOLS_DEBUG") == "1"
SECRET_KEY = os.environ.get("MTOOLS_SECRET_KEY") or (
    "development-only-mtools-key-keep-production-secrets-out-of-source" if DEBUG else ""
)
if not SECRET_KEY:
    raise ImproperlyConfigured("Set MTOOLS_SECRET_KEY.")
ALLOWED_HOSTS = os.environ.get("MTOOLS_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
PUBLIC_ORIGIN = os.environ.get("MTOOLS_PUBLIC_ORIGIN", "http://localhost:5173" if DEBUG else "")
if not DEBUG and not PUBLIC_ORIGIN.startswith("https://"):
    raise ImproperlyConfigured("Set MTOOLS_PUBLIC_ORIGIN to the public HTTPS origin.")
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
INSTALLED_APPS = [
    "django.contrib.auth", "django.contrib.contenttypes", "django.contrib.sessions",
    "django.contrib.staticfiles", "rest_framework", "core",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "core.middleware.PrivateAPI",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates", "APP_DIRS": True}]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("PGDATABASE", "mtools"),
        "USER": os.environ.get("PGUSER", ""),
        "PASSWORD": os.environ.get("PGPASSWORD", ""),
        "HOST": os.environ.get("PGHOST", "127.0.0.1"),
        "PORT": os.environ.get("PGPORT", "5432"),
    }
}
AUTH_USER_MODEL = "core.User"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": f"django.contrib.auth.password_validation.{name}"}
    for name in ("UserAttributeSimilarityValidator", "MinimumLengthValidator",
                 "CommonPasswordValidator", "NumericPasswordValidator")
]
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["core.authentication.WorkbenchSessionAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
USE_TZ = True
TIME_ZONE = "UTC"
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SAMESITE = "Lax"
DATA_UPLOAD_MAX_MEMORY_SIZE = 1_000_000
EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend" if DEBUG
    else "django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = os.environ.get("MTOOLS_SMTP_HOST", "localhost")
EMAIL_PORT = int(os.environ.get("MTOOLS_SMTP_PORT", "587"))
EMAIL_USE_TLS = not DEBUG
EMAIL_HOST_USER = os.environ.get("MTOOLS_SMTP_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("MTOOLS_SMTP_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.environ.get("MTOOLS_FROM_EMAIL", "workbench@localhost")
STATIC_URL = "/assets/"
STATIC_ROOT = ROOT / "staticfiles"
STATICFILES_DIRS = [ROOT / "frontend/dist/assets"] if (ROOT / "frontend/dist/assets").exists() else []
PASSWORD_RESET_TIMEOUT = 3600
CSRF_FAILURE_VIEW = "core.accounts.csrf_failure"
