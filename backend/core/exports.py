import uuid
from decimal import Decimal
from datetime import timedelta

from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import contracts, models, reporting
from .api import InvalidInput, validate_contract, workspace_access


def snapshot(workspace, dataset, locale, template):
    fa = locale == "fa"
    scope = dataset.payload["scope"]
    evidence = dataset.payload["source_ref"]
    ref = {"kind": "dataset", "id": str(dataset.pk), "version": dataset.version}
    cards = []
    rows = dataset.payload["rows"]
    if dataset.schema_id == "numeric_series":
        for item in rows[:12 if template == "detailed" else 3]:
            cards.append({
                "metric_key": item["period_start"], "value": format(Decimal(str(item["value"])), "f") if item["value"] is not None else None,
                "unit": item["unit"], "currency": item["currency"], "scope": scope,
                "basis": "estimate" if dataset.payload["synthetic"] else "observed", "source_ref": evidence,
            })
    model = {
        "artifact_refs": [ref], "template_version": 1, "title": dataset.title, "context": workspace.name,
        "question": "مرور نسخهٔ داده" if fa else "Review the saved dataset",
        "executive_summary": "خلاصهٔ دادهٔ ثبت‌شده" if fa else "Summary of the saved dataset",
        "kpi_cards": cards, "tables": [{"title": dataset.title, "dataset_ref": ref}], "charts": [],
        "decision_ref": None, "action_refs": [], "methodology": [], "assumptions": [], "limitations": [
            ("نمونهٔ مصنوعی است." if fa else "Synthetic example.") if dataset.payload["synthetic"]
            else ("مرور دادهٔ ثبت‌شده." if fa else "Dataset overview."),
        ],
        "evidence_refs": [evidence], "coverage": {
            "status": "draft", "required_method_ids": [], "executed_method_ids": [], "manual_method_ids": [],
            "unavailable_method_ids": [], "missing_requirements": [],
        },
        "locale": locale, "currency": workspace.currency, "timezone": workspace.timezone,
        "generated_at": timezone.now().isoformat(), "status": "demo" if dataset.payload["synthetic"] else "draft",
    }
    model["checksum"] = contracts.digest(model)
    validate_contract("ReportViewModel", model)
    data = [{key: value for key, value in row.items() if key != "source_ref"}
            for row in rows[:40 if template == "detailed" else 8]]
    columns = [
        key for key in contracts.SCHEMA["$defs"]["Row_" + dataset.schema_id]["properties"]
        if any(key in item for item in data)
    ]
    return {"model": model, "template": template, "source": f"{dataset.pk} · v{dataset.version} · {dataset.evidence.title} · {evidence['id']} · v{evidence['version']}",
            "columns": columns, "rows": data}


def public(row):
    newer = models.Dataset.objects.filter(
        workspace_id=row.workspace_id, series=row.source.series, version__gt=row.source.version,
    ).exists()
    return {"id": row.pk, "format": row.format, "state": row.state, "snapshot": row.snapshot["model"], "stale": newer}


@api_view(["GET", "POST"])
@transaction.atomic
def start(request, workspace_id):
    workspace, _ = workspace_access(request, workspace_id, write=request.method == "POST")
    visible = models.ReportExport.objects.filter(workspace=workspace).defer("result").select_related("source")
    if request.method == "GET":
        return Response([public(row) for row in visible.order_by("-created_at")[:100]])
    data = request.data
    if not isinstance(data, dict) or set(data) != {"id", "version", "format", "locale", "template"}:
        raise InvalidInput("Choose a dataset version, format, language and template.")
    try:
        pk = uuid.UUID(data["id"])
    except (ValueError, TypeError, AttributeError):
        raise InvalidInput({"id": "Use a dataset UUID."}) from None
    if (data["format"] not in tuple(reporting.FORMAT_MIME) or data["template"] not in ("executive", "detailed")
            or data["locale"] not in ("fa", "en") or type(data["version"]) is not int):
        raise InvalidInput("Choose supported report options.")
    dataset = get_object_or_404(models.Dataset.objects.select_related("evidence"), workspace=workspace,
                                pk=pk, version=data["version"])
    key = contracts.digest(data)
    existing = visible.filter(request_hash=key).first()
    if existing is not None:
        return Response(public(existing))
    previous = visible.filter(source=dataset, snapshot__template=data["template"],
                              snapshot__model__locale=data["locale"]).order_by("created_at").first()
    report = previous.snapshot if previous is not None else snapshot(workspace, dataset, data["locale"], data["template"])
    row = models.ReportExport.objects.create(
        workspace=workspace, creator=request.user, source=dataset, format=data["format"],
        request_hash=key, snapshot=report,
    )
    return Response(public(row), status=202)


@api_view(["GET"])
def status(request, workspace_id, pk, download=False):
    workspace, _ = workspace_access(request, workspace_id)
    row = get_object_or_404(models.ReportExport.objects.defer("result"), workspace=workspace, pk=pk)
    if not download:
        return Response(public(row))
    if row.state != "succeeded":
        return Response({"code": "report_unavailable"}, status=409)
    return HttpResponse(bytes(row.result), content_type=reporting.FORMAT_MIME[row.format],
                        headers={"Content-Disposition": f'attachment; filename="report-{row.pk}.{row.format}"'})


@transaction.atomic
def claim():
    now = timezone.now()
    pending = models.ReportExport.objects.select_for_update(skip_locked=True).defer("result").filter(
        Q(state="queued") | Q(state="running", lease_until__lte=now),
    ).order_by("created_at")
    for row in pending[:12]:
        if row.attempts >= 3:
            row.state = "failed"
            row.save(update_fields=["state"])
            continue
        row.state, row.lease_token, row.lease_until = "running", uuid.uuid4(), now + timedelta(minutes=2)
        row.attempts += 1
        row.save(update_fields=["state", "lease_token", "lease_until", "attempts"])
        return row
    return None


def process_one():
    row = claim()
    if row is None:
        return False
    try:
        result = reporting.render(row.snapshot, row.format)
    except Exception:
        result = None
    models.ReportExport.objects.filter(pk=row.pk, lease_token=row.lease_token, lease_until__gt=timezone.now()).update(
        state="succeeded" if result else "failed", result=result, lease_until=None, lease_token=None,
    )
    return True
