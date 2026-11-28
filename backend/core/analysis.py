from django.db import transaction
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import artifacts, contracts, jobs, models, preflight as checks, validation
from .api import (Conflict, InvalidInput, Unavailable, audit, fields, form, inspect_contract_values,
                  validate_contract, workspace_access)


@api_view(["GET"])
def tools(request, tool_id=None):
    entries = [
        entry for entry in contracts.CATALOG
        if tool_id in (None, entry["method_id"] if entry["quick"] else entry["tool_id"])
    ]
    if not entries:
        raise Http404
    if tool_id is None:
        return Response(entries)
    return Response({
        "methods": entries,
        "schemas": {entry["method_id"]: contracts.schema_for(entry["input_ref"].split("/")[-1])
                    for entry in entries},
    })


def input_hash(body):
    return contracts.digest({key: value for key, value in body.items() if key != "idempotency_key"})


@api_view(["POST"])
def preflight(request, workspace_id):
    workspace, _ = workspace_access(request, workspace_id)
    method = checks.checked_request(workspace, request.data)
    return Response({
        "availability": method["availability"], "required_for_primary": method["required_for_primary"],
        "missing_fields": checks.missing_requirements(method, request.data["input"]),
        "limitations": [method["release_gate"]],
    })


@api_view(["GET", "POST", "PATCH"])
@transaction.atomic
def drafts(request, workspace_id, pk=None):
    workspace, _ = workspace_access(request, workspace_id, write=request.method != "GET")
    query = models.RunDraft.objects.filter(workspace=workspace, creator=request.user)
    draft = get_object_or_404(query, pk=pk) if pk is not None else None
    if request.method == "GET":
        if draft is not None:
            return Response(fields(draft))
        return Response([fields(row) for row in query.order_by("-created_at", "id")[:200]])
    if (request.method == "PATCH") != (draft is not None):
        return Response({"code": "method_not_allowed"}, status=405)
    body = request.data
    checks.checked_request(workspace, body)
    checksum, key = input_hash(body), body["idempotency_key"]
    duplicate = query.filter(idempotency_key=key).first()
    if duplicate:
        if duplicate.input_hash != checksum or (draft is not None and duplicate.series != draft.series):
            raise Conflict()
        return Response(fields(duplicate))
    revision = {}
    if draft is not None:
        if query.filter(series=draft.series, version__gt=draft.version).exists():
            raise Conflict()
        revision = {"series": draft.series, "version": draft.version + 1}
    saved = query.create(workspace=workspace, creator=request.user, request=body, input_hash=checksum,
                         idempotency_key=key, **revision)
    return Response(fields(saved), status=201)


@api_view(["GET", "POST"])
@transaction.atomic
def runs(request, workspace_id, pk=None):
    workspace, _ = workspace_access(request, workspace_id, write=request.method == "POST")
    query = models.AnalysisRun.objects.filter(workspace=workspace)
    if request.method == "GET":
        if pk is not None:
            return Response(jobs.public_result(get_object_or_404(query, pk=pk)))
        return Response([jobs.public_result(row) for row in query.order_by("-created_at", "id")[:200]])
    if pk is not None:
        return Response({"code": "method_not_allowed"}, status=405)
    body = request.data
    method = checks.checked_request(workspace, body)
    key, checksum = body["idempotency_key"], input_hash(body)
    duplicate = query.filter(idempotency_key=key).first()
    if duplicate:
        if duplicate.input_hash != checksum:
            raise Conflict()
        return Response(jobs.public_result(duplicate))
    if method["availability"] != "active":
        raise Unavailable()
    run = query.create(creator=request.user, workspace=workspace, tool_id=body["tool_id"],
                       method_id=body["method_id"], method_version=body["method_version"],
                       idempotency_key=key, input_snapshot=body, input_hash=checksum)
    models.Job.objects.create(run=run, workspace=workspace, available_at=timezone.now())
    audit(request, workspace, "run_created", run)
    return Response(jobs.public_result(run), status=202)


@api_view(["POST"])
def scratch(request):
    validate_contract("ScratchRequest", request.data)
    inspect_contract_values(None, request.data["input"])
    raise Unavailable()


@api_view(["GET"])
def artifact(request, workspace_id, pk, download=False):
    workspace, _ = workspace_access(request, workspace_id)
    row = get_object_or_404(models.Artifact, workspace=workspace, pk=pk, artifact_type__in=artifacts.PUBLIC_TYPES)
    result = artifacts.envelope(row)
    if download:
        return JsonResponse(result, headers={
            "Content-Disposition": f'attachment; filename="artifact-{row.pk}-v{row.version}.json"',
        })
    return Response(result)


@api_view(["GET"])
def sources(request, workspace_id, pk):
    workspace, _ = workspace_access(request, workspace_id)
    run = get_object_or_404(models.AnalysisRun, workspace=workspace, pk=pk)
    resolved = {}
    inspect_contract_values(workspace, run.input_snapshot, resolved)
    rows = []
    for (kind, ref_id, version), record in resolved.items():
        latest = None
        if isinstance(record, models.Versioned):
            latest = type(record).objects.filter(
                workspace=workspace, series=record.series,
            ).order_by("-version").values_list("version", flat=True).first()
        rows.append({"kind": kind, "id": ref_id, "version": version, "latest_version": latest})
    return Response({"refs": rows, "stale": any((row["latest_version"] or 0) > row["version"] for row in rows)})


@api_view(["GET", "POST"])
@transaction.atomic
def decisions(request, workspace_id):
    workspace, _ = workspace_access(request, workspace_id, write=request.method == "POST")
    query = models.Decision.objects.filter(workspace=workspace)
    if request.method == "GET":
        return Response([fields(row) for row in query.order_by("-created_at", "id")[:200]])
    data = form(validation.DecisionInput, request.data)
    run = get_object_or_404(models.AnalysisRun, workspace=workspace, pk=data["run_id"])
    if run.status != "succeeded" or run.result["analysis_status"] not in ("ready", "conditional") or not any(
        option["id"] == data["selected_option"] for option in run.result["options"]
    ):
        raise InvalidInput({"selected_option": "Select an option from a completed analysis."})
    saved = query.create(workspace=workspace, created_by=request.user, **data)
    audit(request, workspace, "decision_drafted", saved)
    return Response(fields(saved), status=201)


@api_view(["POST"])
@transaction.atomic
def approve(request, workspace_id, pk):
    workspace, _ = workspace_access(request, workspace_id, write=True, owner=True)
    decision = get_object_or_404(models.Decision, workspace=workspace, pk=pk)
    if request.data:
        raise InvalidInput("Approval takes no client-supplied state.")
    if decision.state == "approved":
        return Response(fields(decision))
    if decision.state != "draft":
        raise Conflict()
    decision.state, decision.approved_at, decision.approved_by = "approved", timezone.now(), request.user
    decision.save(update_fields=["state", "approved_at", "approved_by"])
    audit(request, workspace, "decision_approved", decision)
    return Response(fields(decision))
