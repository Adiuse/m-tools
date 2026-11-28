import math
from decimal import Decimal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException, PermissionDenied
from rest_framework.response import Response

from . import contracts, models, validation


class InvalidInput(APIException):
    status_code = 422
    default_detail = "Invalid input."


class Conflict(APIException):
    status_code = 409
    default_detail = "The current version or idempotency key conflicts with this request."


class Unavailable(APIException):
    status_code = 503
    default_detail = "This method is planned and cannot be run yet."


def form(serializer_class, data):
    serializer = serializer_class(data=data)
    if not serializer.is_valid():
        raise InvalidInput({"fields": serializer.errors})
    return serializer.validated_data


def validate_contract(name, data):
    error = contracts.validate(name, data)
    if error is not None:
        raise InvalidInput({"contract": name, "field": ".".join(map(str, error.absolute_path)) or "body"})


def workspace_access(request, workspace_id, *, write=False, owner=False):
    workspaces = models.Workspace.objects.filter(membership__user=request.user, membership__active=True)
    if write:
        workspaces = workspaces.select_for_update(of=("self",))
    workspace = get_object_or_404(workspaces, pk=workspace_id)
    role = get_object_or_404(models.Membership, workspace=workspace, user=request.user, active=True).role
    if (write and role == models.Membership.Role.VIEWER) or (owner and role != models.Membership.Role.OWNER):
        raise PermissionDenied()
    return workspace, role


def fields(instance, *excluded):
    result = {}
    for field in instance._meta.concrete_fields:
        key = field.attname
        if key not in excluded:
            value = field.value_from_object(instance)
            if isinstance(value, Decimal):
                decimal = format(value, "f")
                value = decimal.rstrip("0").rstrip(".") if "." in decimal else decimal
            result[key] = value
    return result


def audit(request, workspace, action, entity):
    models.AuditEvent.objects.create(actor=request.user, workspace=workspace, action=action, entity_id=entity.pk)


@api_view(["GET", "POST"])
@transaction.atomic
def workspaces(request):
    if request.method == "GET":
        memberships = models.Membership.objects.filter(user=request.user, active=True).select_related("workspace")
        return Response([{**fields(m.workspace), "role": m.role} for m in memberships.order_by("workspace__name")])
    info = form(validation.WorkspaceInput, request.data)
    company = models.Workspace.objects.create(**{key: info.pop(key) for key in ("name", "currency", "timezone")})
    models.Membership.objects.create(workspace=company, user=request.user, role=models.Membership.Role.OWNER)
    models.CompanyProfile.objects.create(workspace=company, **info)
    audit(request, company, "workspace_created", company)
    return Response({**fields(company), "role": models.Membership.Role.OWNER}, status=201)


@api_view(["GET", "POST"])
@transaction.atomic
def memberships(request, workspace_id):
    workspace, _ = workspace_access(request, workspace_id, write=request.method == "POST", owner=True)
    if request.method == "GET":
        return Response([
            {"id": member.user_id, "email": member.user.email, "role": member.role, "active": member.active}
            for member in models.Membership.objects.filter(workspace=workspace).select_related("user")
        ])
    data = form(validation.MembershipInput, request.data)
    user = get_object_or_404(models.User, email=data["email"].lower(), is_active=True)
    role, active = data["role"], data["active"]
    if not active or role != models.Membership.Role.OWNER:
        other_owners = models.Membership.objects.filter(
            workspace=workspace, role=models.Membership.Role.OWNER, active=True,
        ).exclude(user=user)
        if not other_owners.exists():
            raise Conflict("Keep at least one active workspace owner.")
    membership, _ = models.Membership.objects.update_or_create(
        workspace=workspace, user=user, defaults={"role": role, "active": active},
    )
    audit(request, workspace, "membership_updated", user)
    return Response({"id": user.pk, "email": user.email, "role": membership.role, "active": membership.active})


ENTITIES = {
    "profiles": (models.CompanyProfile, validation.ProfileInput),
    "evidence": (models.Evidence, validation.EvidenceInput),
    "datasets": (models.Dataset, validation.DatasetInput),
    "metrics": (models.MetricDefinition, validation.MetricInput),
    "observations": (models.Observation, validation.ObservationInput),
    "goals": (models.Goal, validation.GoalInput),
    "hypotheses": (models.Hypothesis, validation.HypothesisInput),
    "actions": (models.Action, validation.ActionInput),
    "outcomes": (models.Outcome, validation.OutcomeInput),
}
REF_MODELS = {
    "profile": models.CompanyProfile, "evidence": models.Evidence, "dataset": models.Dataset,
    "metric": models.MetricDefinition, "observation": models.Observation, "goal": models.Goal,
    "hypothesis": models.Hypothesis, "analysis_run": models.AnalysisRun, "decision": models.Decision,
    "action": models.Action, "outcome": models.Outcome, "artifact": models.Artifact,
}


def resolve_ref(workspace, ref):
    kind, pk, version = ref["kind"], ref["id"], ref["version"]
    if kind == "workspace" and str(workspace.pk) == pk.lower() and version == 1:
        return workspace
    if kind == "user" and version == 1:
        return get_object_or_404(models.Membership, workspace=workspace, user_id=pk, active=True).user
    model = REF_MODELS.get(kind)
    if model is None:
        raise Http404
    queryset = model.objects.filter(workspace=workspace)
    if model is models.Artifact:
        from .artifacts import PUBLIC_TYPES
        queryset = queryset.filter(artifact_type__in=PUBLIC_TYPES)
    if issubclass(model, models.Versioned):
        queryset = queryset.filter(version=version)
    elif version != 1:
        raise Http404
    return get_object_or_404(queryset, pk=pk)


def inspect_contract_values(workspace, value, refs=None):
    if refs is None:
        refs = {}
    if isinstance(value, dict):
        if set(value) == {"kind", "id", "version"}:
            validate_contract("Ref", value)
            if workspace is None:
                raise InvalidInput("Scratch inputs cannot contain workspace references.")
            key = (value["kind"], value["id"], value["version"])
            if key not in refs:
                refs[key] = resolve_ref(workspace, value)
            return
        if set(value) == {"start", "end_exclusive", "timezone"}:
            validate_contract("Period", value)
            if value["start"] >= value["end_exclusive"]:
                raise InvalidInput({"period": "The exclusive end must follow the start."})
            try:
                ZoneInfo(value["timezone"])
            except (ValueError, ZoneInfoNotFoundError):
                raise InvalidInput({"timezone": "Use an IANA timezone."}) from None
        for key, nested in value.items():
            inspect_contract_values(workspace, key, refs)
            inspect_contract_values(workspace, nested, refs)
    elif isinstance(value, list):
        for nested in value:
            inspect_contract_values(workspace, nested, refs)
    elif isinstance(value, str):
        try:
            value.encode("utf-8")
        except UnicodeEncodeError:
            raise InvalidInput("Use valid Unicode input.") from None
        if "\x00" in value:
            raise InvalidInput("Null characters are invalid.")
    elif isinstance(value, float) and not math.isfinite(value):
        raise InvalidInput("Numeric values must be finite.")


def dataset_values(workspace, document):
    validate_contract("DatasetPayload", document)
    if document["workspace_id"].lower() != str(workspace.pk):
        raise Http404
    if len(document["rows"]) > 2000:
        raise InvalidInput({"rows": "Enter at most 2000 rows in one manual dataset."})
    if document["source_ref"]["kind"] != "evidence":
        raise InvalidInput({"source_ref": "Supply an evidence reference."})
    evidence = resolve_ref(workspace, document["source_ref"])
    if (evidence.kind == "assumption" or evidence.claim_only) and not document["synthetic"]:
        raise InvalidInput({"source_ref": "Observed data requires a source other than an assumption."})
    inspect_contract_values(workspace, document["scope"])
    inspect_contract_values(workspace, document["columns"])
    row_state = {}
    refs = {}
    for row in document["rows"]:
        validate_dataset_row(workspace, document, row, row_state, refs)
    return {
        "evidence": evidence, "schema_id": document["schema_id"], "schema_version": document["schema_version"],
        "row_count": len(document["rows"]), "checksum": contracts.digest(document),
    }


def validate_dataset_row(workspace, document, row, seen, refs):
    inspect_contract_values(workspace, row, refs)
    source_ref = row["source_ref"]
    if source_ref["kind"] != "evidence":
        raise InvalidInput("Each row source must reference evidence.")
    source = refs[(source_ref["kind"], source_ref["id"], source_ref["version"])]
    if not document["synthetic"] and (source.kind == "assumption" or source.claim_only):
        raise InvalidInput("Observed rows require evidence.")

    schema = document["schema_id"]
    scope = document["scope"]
    if schema == "numeric_series":
        key = (row["series_key"], row["period_start"])
        value = row["value"]
        period = scope["period"]
        if row["unit"] != scope["unit"] or not period["start"] <= row["period_start"] < period["end_exclusive"]:
            raise InvalidInput("Row unit and date must match the dataset scope.")
        currency_key = ("currency", row["series_key"])
        if currency_key in seen and seen[currency_key] != row["currency"]:
            raise InvalidInput("A numeric series must use a consistent currency.")
    elif schema == "metric_observations":
        metric_ref = row["metric_ref"]
        if metric_ref["kind"] != "metric":
            raise InvalidInput("The observation must reference a metric definition.")
        metric = refs[(metric_ref["kind"], metric_ref["id"], metric_ref["version"])]
        if row["unit"] != scope["unit"] or row["unit"] != metric.unit or row["grain"] != scope["grain"] or row["grain"] != metric.grain:
            raise InvalidInput("Observation unit and grain must match the metric and dataset.")
        period = row["period"]
        scope_period = scope["period"]
        if (period["timezone"] != scope_period["timezone"] or period["start"] < scope_period["start"]
                or period["end_exclusive"] > scope_period["end_exclusive"]):
            raise InvalidInput("Observation period must fit within the dataset scope.")
        value = Decimal(row["value"]) if row["value"] is not None else None
        if (value is None) != bool(row["missing_reason"]):
            raise InvalidInput("A missing value requires a reason; a recorded zero is a value.")
        key = (row["observation_key"],)
    elif schema == "events":
        key = (row["event_key"],)
        value = None
    elif schema == "graph_nodes":
        key = (row["node_key"],)
        value = None
    else:
        return

    if value is not None and row["unit"] == "count" and (value < 0 or value % 1 != 0):
        raise InvalidInput("Count must be a nonnegative integer.")
    if key in seen:
        raise InvalidInput("Duplicate dataset row key.")
    seen[key] = True
    if schema == "numeric_series":
        seen[currency_key] = row["currency"]



def scoped_relations(model, workspace, data):
    for field in model._meta.concrete_fields:
        if field.attname not in data or data[field.attname] is None or not field.is_relation:
            continue
        related = field.related_model
        if issubclass(related, models.TenantRow):
            get_object_or_404(related, workspace=workspace, pk=data[field.attname])
        elif related is models.User:
            get_object_or_404(models.Membership, workspace=workspace, user_id=data[field.attname], active=True)


def entity_values(kind, model, request, workspace, previous=None):
    serializer_class = ENTITIES[kind][1]
    body = request.data
    if previous is not None and isinstance(body, dict):
        current = fields(previous)
        body = {**{key: current[key] for key in serializer_class().fields if key in current}, **body}
    data = form(serializer_class, body)
    if kind != "datasets":
        inspect_contract_values(workspace, data)
    scoped_relations(model, workspace, data)
    if kind == "evidence":
        data.update(created_by=request.user, checksum=contracts.digest(data),
                    claim_only=previous.claim_only if previous is not None else False)
    elif kind == "datasets":
        if previous is not None and isinstance(data["payload"], dict) and (
            previous.payload["synthetic"] != data["payload"].get("synthetic")
        ):
            raise InvalidInput({"synthetic": "A dataset series retains its synthetic provenance."})
        data.update(created_by=request.user, **dataset_values(workspace, data["payload"]))
    elif kind == "observations":
        evidence = models.Evidence.objects.get(pk=data["evidence_id"])
        dataset = models.Dataset.objects.filter(pk=data.get("dataset_id")).first()
        if evidence.kind == "assumption" or evidence.claim_only or (dataset is not None and dataset.payload["synthetic"]):
            raise InvalidInput("Observed values require evidence and non-synthetic data.")
        identifying = ("metric_id", "period_start", "period_end")
        if previous is not None and (
            any(data[key] != getattr(previous, key) for key in identifying)
            or data.get("dimensions", {}) != previous.dimensions
        ):
            raise InvalidInput("Create a new observation when its metric, period or dimensions change.")
        value = data["value"]
        metric = models.MetricDefinition.objects.get(pk=data["metric_id"])
        if metric.unit == "count" and value is not None and (value < 0 or value != value.to_integral_value()):
            raise InvalidInput({"value": "Count must be a nonnegative integer."})
        data.update(dimensions_hash=contracts.digest(data.get("dimensions", {})))
        version = previous.version + 1 if previous is not None else 1
        grain = ("metric_id", "period_start", "period_end", "dimensions_hash")
        if models.Observation.objects.filter(workspace=workspace, version=version,
                                             **{field: data[field] for field in grain}).exists():
            raise Conflict("This metric and observation scope already exist.")
    elif kind == "goals":
        baseline = models.Observation.objects.filter(pk=data.get("baseline_id")).first()
        if baseline is not None and baseline.metric_id != data["metric_id"]:
            raise InvalidInput({"baseline_id": "Baseline and goal must use the same metric version."})
        data.update(owner=request.user)
    elif kind == "actions":
        if models.Decision.objects.get(pk=data["decision_id"]).state != "approved":
            raise Conflict("Approve the decision before scheduling an action.")
    return data


def entity_model(kind):
    try:
        return ENTITIES[kind][0]
    except KeyError:
        raise Http404 from None


@api_view(["GET", "POST"])
@transaction.atomic
def entities(request, workspace_id, kind):
    workspace, _ = workspace_access(request, workspace_id, write=request.method == "POST")
    return workspace_entities(request, workspace, kind)


def workspace_entities(request, workspace, kind):
    model = entity_model(kind)
    query = model.objects.filter(workspace=workspace)
    if request.method == "GET":
        return Response([fields(record) for record in query.order_by("-created_at", "id")[:200]])
    if kind == "profiles" and query.exists():
        raise Conflict("Update the existing company profile to create a new version.")
    record = model.objects.create(workspace=workspace, **entity_values(kind, model, request, workspace))
    audit(request, workspace, f"{kind}_created", record)
    return Response(fields(record), status=201)


@api_view(["GET", "PATCH"])
@transaction.atomic
def entity(request, workspace_id, kind, pk):
    workspace, _ = workspace_access(request, workspace_id, write=request.method == "PATCH")
    model = entity_model(kind)
    record = get_object_or_404(model, workspace=workspace, pk=pk)
    if request.method == "GET":
        return Response(fields(record))
    if model.objects.filter(workspace=workspace, series=record.series, version__gt=record.version).exists():
        raise Conflict()
    updated = model.objects.create(workspace=workspace, series=record.series, version=record.version + 1,
                                   **entity_values(kind, model, request, workspace, previous=record))
    audit(request, workspace, f"{kind}_revised", updated)
    return Response(fields(updated), status=201)


@api_view(["GET"])
def history(request, workspace_id):
    workspace, _ = workspace_access(request, workspace_id)
    rows = models.AuditEvent.objects.filter(workspace=workspace).order_by("-created_at", "id")[:200]
    return Response([fields(row) for row in rows])
