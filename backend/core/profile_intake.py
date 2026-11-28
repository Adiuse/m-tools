import hashlib
import io
from datetime import timedelta
from html.parser import HTMLParser
from pathlib import Path

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.decorators import api_view, parser_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from . import contracts, models
from .accounts import allowed
from .api import Conflict, InvalidInput, audit, fields, form, workspace_access
from .dataset_intake import get_preview
from .intake_files import IntakeError, check_package, read_upload, rows_from_file
from .public_source import public_page
from .validation import ProfileInput

KEYS = {
    "industry": ("industry", "نوع فعالیت"),
    "offering": ("offering", "product", "محصول", "خدمت"),
    "objective": ("objective", "هدف"),
    "business_model": ("business model", "مدل کسب‌وکار"),
    "geography": ("geography", "بازار جغرافیایی"),
}


class TextNodes(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lines = []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "template"):
            self.hidden += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style", "template") and self.hidden:
            self.hidden -= 1

    def handle_data(self, data):
        if not self.hidden and data.strip():
            self.lines.extend(data.splitlines())


def units(raw, extension):
    if extension in (".txt", ".html"):
        text = raw.decode("utf-8-sig")
        if extension == ".html":
            parser = TextNodes()
            parser.feed(text)
            text = "\n".join(parser.lines)
        yield from ((f"line:{index}", line) for index, line in enumerate(text.splitlines(), 1))
    elif extension in (".xlsx", ".csv"):
        for index, row in enumerate(rows_from_file(raw, extension), 1):
            values = [str(cell) for cell in row if cell is not None]
            if len(values) == 2:
                yield f"row:{index}", ": ".join(values)
            else:
                yield f"row:{index}", " ".join(values)
    elif extension == ".pdf":
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(raw))
        if reader.is_encrypted or len(reader.pages) > 30:
            raise IntakeError("Use a text PDF with up to 30 pages.")
        for index, page in enumerate(reader.pages, 1):
            for offset, line in enumerate((page.extract_text() or "").splitlines(), 1):
                yield f"page:{index}/line:{offset}", line
    elif extension == ".docx":
        from docx import Document
        check_package(raw)
        for index, paragraph in enumerate(Document(io.BytesIO(raw)).paragraphs, 1):
            yield f"paragraph:{index}", paragraph.text
    elif extension == ".pptx":
        from pptx import Presentation
        check_package(raw)
        for index, slide in enumerate(Presentation(io.BytesIO(raw)).slides, 1):
            for offset, shape in enumerate(slide.shapes, 1):
                if shape.has_text_frame:
                    for line in shape.text.splitlines():
                        yield f"slide:{index}/shape:{offset}", line
    else:
        raise IntakeError("Choose PDF, DOCX, XLSX, PPTX, text or CSV.")


def suggestions(raw, extension, profile):
    labels = {label: key for key, names in KEYS.items() for label in names}
    offered = {}
    for index, (anchor, line) in enumerate(units(raw, extension)):
        if index > 5000:
            raise IntakeError("The source contains too much text.")
        label, sep, content = line.partition(":")
        name = labels.get(label.strip().casefold())
        content = content.strip()
        if not sep or not name or not content or name in offered:
            continue
        spec = ProfileInput().fields[name]
        if len(content) > spec.max_length or any(ord(char) < 32 for char in content):
            continue
        offered[name] = {"field": name, "proposed": content, "current": getattr(profile, name),
                         "anchor": anchor, "excerpt_hash": hashlib.sha256(line.encode()).hexdigest()}
    return {"fields": list(offered.values()), "missing_fields": sorted(KEYS.keys() - offered.keys())}


@api_view(["POST"])
@parser_classes([MultiPartParser])
def preview(request, workspace_id):
    workspace, role = workspace_access(request, workspace_id)
    if role == "viewer":
        raise PermissionDenied()
    if request.data.get("authorized") != "yes":
        raise InvalidInput("Confirm permission to use the source.")
    if models.IntakePreview.objects.filter(
        workspace=workspace, creator=request.user, kind="profile", created_at__gte=timezone.now() - timedelta(minutes=1),
    ).count() >= 5:
        return Response({"code": "rate_limited"}, status=429)
    current = models.CompanyProfile.objects.filter(workspace=workspace).order_by("-version").first()
    if current is None:
        raise Conflict("Create a company profile before reviewing a source.")
    source = request.data.get("url", "")
    if source and not allowed("profile-source", str(request.user.pk)):
        return Response({"code": "rate_limited"}, status=429)
    upload = request.FILES.get("file")
    if bool(source) == bool(upload):
        raise InvalidInput("Choose exactly one source.")
    try:
        if source:
            if len(source) > 200:
                raise IntakeError("Use a shorter source URL.")
            raw, mime = public_page(source)
            extension = ".html" if mime == "text/html" else ".txt"
            title = "Public company website"
        else:
            raw = read_upload(upload)
            extension = Path(upload.name).suffix.lower()
            title = upload.name[:200]
        output = suggestions(raw, extension, current)
    except Exception as exc:
        if isinstance(exc, IntakeError):
            raise InvalidInput(str(exc)) from None
        raise InvalidInput("Use a readable, unencrypted document with selectable text.") from None
    entry = models.IntakePreview.objects.create(
        workspace=workspace, creator=request.user, kind="profile", checksum=hashlib.sha256(raw).hexdigest(),
        payload={**output, "base_id": str(current.pk), "base_version": current.version,
                 "source": source, "title": title, "source_type": extension[1:]},
        expires_at=timezone.now() + timedelta(hours=1),
    )
    return Response({"id": entry.pk, "checksum": entry.checksum, **entry.payload}, status=201)


@api_view(["POST"])
@transaction.atomic
def apply(request, workspace_id, pk):
    workspace, _ = workspace_access(request, workspace_id, write=True)
    entry = get_preview(workspace, request.user, pk, "profile")
    body = request.data
    if (not isinstance(body, dict) or set(body) != {"confirm", "checksum", "expected_version", "fields"}
            or body["confirm"] is not True or body["checksum"] != entry.checksum):
        raise InvalidInput("Confirm the reviewed source.")
    choices = body.get("fields")
    candidate = {item["field"]: item["proposed"] for item in entry.payload["fields"]}
    if (not isinstance(choices, dict) or not choices or set(choices) - candidate.keys()
            or any(not isinstance(value, str) for value in choices.values())):
        raise InvalidInput("Choose only fields explicitly identified in this source.")
    if entry.applied_id:
        existing = get_object_or_404(models.CompanyProfile, workspace=workspace, pk=entry.applied_id)
        if entry.payload.get("applied_hash") != contracts.digest(choices):
            raise Conflict()
        evidence = get_object_or_404(models.Evidence, workspace=workspace, pk=entry.payload["evidence_id"])
        return Response(applied_profile(entry, existing, evidence, choices))
    current = models.CompanyProfile.objects.filter(workspace=workspace).order_by("-version").first()
    if current is None or str(current.pk) != entry.payload["base_id"] or body.get("expected_version") != current.version:
        raise Conflict("Stage the source again against the latest profile.")
    values = {key: getattr(current, key) for key in ProfileInput().fields}
    checked = form(ProfileInput, {**values, **choices})
    evidence = models.Evidence.objects.create(
        workspace=workspace, kind="secondary" if entry.payload["source"] else "internal",
        title=entry.payload["title"], source_uri=entry.payload["source"], collected_at=timezone.localdate(),
        checksum=entry.checksum, created_by=request.user, scope="Company profile review",
        quality_notes="User-reviewed source. " + "; ".join(
            f"{item['field']} ({item['anchor']}, SHA-256 {item['excerpt_hash']})"
            for item in entry.payload["fields"] if item["field"] in choices
        ),
    )
    profile = models.CompanyProfile.objects.create(
        workspace=workspace, series=current.series, version=current.version + 1, **checked,
    )
    entry.applied_id = profile.pk
    entry.payload.update(evidence_id=str(evidence.pk), applied_hash=contracts.digest(choices))
    entry.save(update_fields=["applied_id", "payload"])
    audit(request, workspace, "profile_intake_applied", profile)
    return Response(applied_profile(entry, profile, evidence, choices), status=201)


def applied_profile(entry, profile, evidence, choices):
    return {"profile": fields(profile), "evidence": fields(evidence), "anchors": [
        item for item in entry.payload["fields"] if item["field"] in choices
    ]}
