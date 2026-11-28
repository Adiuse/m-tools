import hashlib
import subprocess
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

from . import artifacts, contracts, models, provenance, reporting
from .api import InvalidInput, inspect_contract_values, resolve_ref, validate_contract, workspace_access


SECTIONS = ("summary", "kpis", "tables", "charts", "methodology")


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
        "kpi_cards": cards, "tables": [{"title": dataset.title, "dataset_ref": ref}], "charts": (
            [{"type": "line", "title": dataset.title, "dataset_ref": ref, "x_key": "period_start",
              "y_keys": ["value"], "legend": [scope["unit"]]}]
            if dataset.schema_id == "numeric_series" and len({row["series_key"] for row in rows}) == 1 else []
        ),
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
    return freeze(workspace, model, template)


def freeze(workspace, model, template):
    model = {key: value for key, value in model.items() if key != "checksum"}
    model["checksum"] = contracts.digest(model)
    validate_contract("ReportViewModel", model)
    refs = {}
    inspect_contract_values(workspace, model, refs)
    if model["status"] != "demo" and provenance.has_synthetic_source(refs.values()):
        raise InvalidInput("Reports using synthetic data must carry demo status.")
    try:
        provenance.validate_observed(workspace, model)
    except ValueError as exc:
        raise InvalidInput(str(exc)) from None
    limit = 40 if template == "detailed" else 8
    tables, charts = [], []
    report_refs = [*model["artifact_refs"], *model["evidence_refs"]]

    def dataset_for(item):
        ref = item["dataset_ref"]
        if ref["kind"] != "dataset":
            raise InvalidInput({"dataset_ref": "Select a versioned dataset."})
        report_refs.append(ref)
        dataset = resolve_ref(workspace, ref)
        report_refs.append(dataset.payload["source_ref"])
        report_refs.extend(row["source_ref"] for row in dataset.payload["rows"][:limit])
        return dataset

    for table in model["tables"]:
        dataset = dataset_for(table)
        columns = [key for key in contracts.SCHEMA["$defs"]["Row_" + dataset.schema_id]["properties"]
                   if key != "source_ref"]
        data = dataset.payload["rows"][:limit]
        fields = contracts.SCHEMA["$defs"]["Row_" + dataset.schema_id]["properties"]
        tables.append({"title": table["title"], "columns": columns,
                       "date_columns": [key for key in columns if fields[key].get("format") == "date"],
                       "total_rows": dataset.row_count,
                       "rows": [{key: row.get(key) for key in columns} for row in data]})
    for spec in model["charts"]:
        dataset = dataset_for(spec)
        keys = [spec["x_key"], *spec["y_keys"]]
        properties = contracts.SCHEMA["$defs"]["Row_" + dataset.schema_id]["properties"]
        if len(set(keys)) != len(keys) or any(key not in properties or key == "source_ref" for key in keys):
            raise InvalidInput({"charts": "The chart columns must match the source dataset."})
        chart_rows = [[row.get(key) for key in keys] for row in dataset.payload["rows"][:limit]]
        numeric = len(keys) > 1 and bool(chart_rows) and all(
            type(value) in (int, float) or value is None for row in chart_rows for value in row[1:]
        )
        charts.append({"title": spec["title"], "type": spec["type"],
                       "columns": [keys[0], *(spec["legend"] or keys[1:])][:len(keys)]
                       if len(spec["legend"]) == len(keys) - 1 else keys,
                       "rows": chart_rows, "total_rows": dataset.row_count, "numeric": numeric})
    sources = []
    unique_refs = {}
    for ref in report_refs:
        unique_refs.setdefault((ref["kind"], ref["id"], ref["version"]), ref)
    for ref in unique_refs.values():
        record = resolve_ref(workspace, ref)
        title = getattr(record, "title", "")
        sources.append(f"{ref['kind']} · {ref['id']} · v{ref['version']}" + (f" · {title}" if title else ""))
    return {"model": model, "template": template, "source": " | ".join(sources),
            "tables": tables, "charts": charts, "source_refs": list(unique_refs.values())}


def public(row):
    source = row.source or row.source_artifact
    newer = type(source).objects.filter(
        workspace_id=row.workspace_id, series=source.series, version__gt=source.version,
    ).exists()
    return {"id": row.pk, "format": row.format, "state": row.state, "snapshot": row.snapshot["model"],
            "stale": newer, "expires_at": row.expires_at, "checksum": row.checksum,
            "renderer_version": row.renderer_version, "error_code": row.error_code or None}


@api_view(["GET", "POST"])
@transaction.atomic
def start(request, workspace_id):
    workspace, _ = workspace_access(request, workspace_id, write=request.method == "POST")
    visible = models.ReportExport.objects.filter(workspace=workspace).defer("result").select_related("source", "source_artifact")
    if request.method == "GET":
        return Response([public(row) for row in visible.order_by("-created_at")[:100]])
    data = request.data
    fields = {"id", "version", "format", "locale", "template"}
    if not isinstance(data, dict) or not fields <= data.keys() or data.keys() - fields - {"artifact_type", "include_sections"}:
        raise InvalidInput("Choose a dataset version, format, language and template.")
    try:
        pk = uuid.UUID(data["id"])
    except (ValueError, TypeError, AttributeError):
        raise InvalidInput({"id": "Use a versioned source UUID."}) from None
    if (data["format"] not in tuple(reporting.FORMAT_MIME) or data["template"] not in ("executive", "detailed")
            or data["locale"] not in ("fa", "en") or type(data["version"]) is not int):
        raise InvalidInput("Choose supported report options.")
    requested = data.get("include_sections", list(SECTIONS))
    if not isinstance(requested, list) or not all(isinstance(item, str) and item in SECTIONS for item in requested):
        raise InvalidInput({"include_sections": "Choose report sections."})
    sections = [name for name in SECTIONS if name in requested]
    source_type = data.get("artifact_type", "dataset")
    if source_type == "dataset":
        record = get_object_or_404(models.Dataset, workspace=workspace, pk=pk, version=data["version"])
        relation = {"source": record}
    elif source_type == "ReportViewModel":
        record = get_object_or_404(models.Artifact, workspace=workspace, pk=pk, version=data["version"],
                                   artifact_type="ReportViewModel")
        relation = {"source_artifact": record}
    else:
        raise InvalidInput({"artifact_type": "Choose a dataset or ReportViewModel source."})
    key = contracts.digest({**data, "id": str(pk), "artifact_type": source_type, "include_sections": sections})
    now = timezone.now()
    existing = visible.filter(request_hash=key).first()
    if existing is not None:
        expiry = existing.expires_at or (existing.created_at + timedelta(hours=1) if existing.state == "succeeded" else None)
        if expiry is None or expiry > now:
            return Response(public(existing))
        existing.delete()
    previous = visible.filter(**relation, snapshot__tables__isnull=False, snapshot__template=data["template"],
                              snapshot__model__locale=data["locale"]).order_by("created_at").first()
    if previous is not None:
        report = previous.snapshot
    elif source_type == "dataset":
        report = snapshot(workspace, record, data["locale"], data["template"])
    else:
        model = artifacts.envelope(record)["payload"]
        report = freeze(workspace, {**model, "locale": data["locale"]}, data["template"])
    report = {**report, "include_sections": sections}
    row = models.ReportExport.objects.create(
        workspace=workspace, creator=request.user, format=data["format"],
        request_hash=key, snapshot=report, **relation,
    )
    return Response(public(row), status=202)


@api_view(["GET"])
def sources(request, workspace_id):
    workspace, _ = workspace_access(request, workspace_id)
    datasets = models.Dataset.objects.filter(workspace=workspace).order_by("-created_at")[:100]
    saved = models.Artifact.objects.filter(workspace=workspace, artifact_type="ReportViewModel").order_by("-created_at")[:100]
    return Response([
        {"id": row.pk, "title": row.title, "version": row.version, "artifact_type": "dataset",
         "synthetic": row.payload["synthetic"]} for row in datasets
    ] + [
        {"id": row.pk, "title": row.payload["title"], "version": row.version,
         "artifact_type": row.artifact_type, "synthetic": row.payload["status"] == "demo"} for row in saved
        if isinstance(row.payload, dict) and not contracts.validate("ReportViewModel", row.payload)
    ])


@api_view(["GET"])
def status(request, workspace_id, pk, download=False):
    workspace, _ = workspace_access(request, workspace_id)
    row = get_object_or_404(models.ReportExport.objects.defer("result"), workspace=workspace, pk=pk)
    if not download:
        return Response(public(row))
    if row.state != "succeeded":
        return Response({"code": "report_unavailable"}, status=409)
    lifetime = row.expires_at or row.created_at + timedelta(hours=1)
    if lifetime <= timezone.now():
        return Response({"code": "report_expired"}, status=410)
    inspect_contract_values(workspace, row.snapshot.get("source_refs", []))
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
            row.state, row.expires_at = "failed", now + timedelta(hours=1)
            row.lease_token = row.lease_until = None
            row.error_code = "lease_exhausted"
            row.save(update_fields=["state", "expires_at", "lease_token", "lease_until", "error_code"])
            continue
        row.state, row.lease_token, row.lease_until = "running", uuid.uuid4(), now + timedelta(minutes=2)
        row.attempts += 1
        row.save(update_fields=["state", "lease_token", "lease_until", "attempts"])
        return row
    return None


def prune_expired():
    now = timezone.now()
    past_deadline = Q(expires_at__lte=now) | Q(state="succeeded", expires_at__isnull=True, created_at__lte=now - timedelta(hours=1))
    expired = list(models.ReportExport.objects.filter(past_deadline).exclude(state="running")
                   .order_by("expires_at").values_list("pk", flat=True)[:100])
    if expired:
        models.ReportExport.objects.filter(past_deadline, pk__in=expired).exclude(state="running").delete()
    abandoned = list(models.IntakePreview.objects.filter(expires_at__lte=now, applied_id__isnull=True)
                     .order_by("expires_at").values_list("pk", flat=True)[:100])
    if abandoned:
        models.IntakePreview.objects.filter(pk__in=abandoned, expires_at__lte=now, applied_id__isnull=True).delete()


def process_one():
    row = claim()
    if row is None:
        return False
    authorized = models.Membership.objects.filter(
        workspace_id=row.workspace_id, user_id=row.creator_id, active=True, role__in=["owner", "editor"],
    ).exists()
    result, retry, version = None, False, ""
    error_code = "" if authorized else "membership_required"
    if authorized:
        try:
            inspect_contract_values(row.workspace, row.snapshot.get("source_refs", []))
            version = reporting.renderer_version(row.format)
            result = reporting.render(row.snapshot, row.format)
        except (OSError, subprocess.TimeoutExpired):
            retry = row.attempts < 3
            error_code = "renderer_unavailable"
        except Exception:
            error_code = "render_failed"
    state = "succeeded" if result else "queued" if retry else "failed"
    models.ReportExport.objects.filter(pk=row.pk, lease_token=row.lease_token, lease_until__gt=timezone.now()).update(
        state=state, result=result, checksum=hashlib.sha256(result).hexdigest() if result else "",
        renderer_version=version, error_code=error_code,
        expires_at=timezone.now() + timedelta(hours=1) if not retry else None, lease_until=None, lease_token=None,
    )
    return True
