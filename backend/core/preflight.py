"""Shared catalog and reference preflight for proposed analysis inputs."""

from django.http import Http404
from django.shortcuts import get_object_or_404

from . import contracts, models, provenance
from .api import InvalidInput, inspect_contract_values, resolve_ref, validate_contract


def value_at(data, path):
    for key in path.split("."):
        if not isinstance(data, dict):
            return None
        data = data.get(key)
    return data


def present(value):
    return value is not None and value != [] and value != {} and (
        not isinstance(value, str) or bool(value.strip())
    )


# These entries describe alternatives in prose in the approved catalog.
# Each tuple contains the fields required for one alternative.
ALTERNATIVES = {
    "at least one complete metric input pair": (
        ("revenue", "variable_cost"), ("acquisition_cost", "new_customers"),
        ("incremental_margin", "campaign_cost"), ("cohorts",),
    ),
    "one complete requested ratio": (
        ("impressions", "clicks"), ("clicks", "conversion_count"), ("clicks", "conversion_credit"),
        ("clicks", "cost"), ("impressions", "cost"), ("conversion_count", "cost"), ("conversion_credit", "cost"),
    ),
    "one contribution representation": (
        ("expected_contribution_per_initial",), ("contribution_per_active", "survival"),
        ("contribution_per_initial",), ("steady_contribution",),
    ),
    "m/p/q OR data": (("m", "p", "q"), ("first_adopters_ref",), ("adopters",)),
}


def missing_requirements(method, values):
    missing = []
    for requirement in method["required_for_primary"]:
        alternatives = ALTERNATIVES.get(requirement) or [
            tuple(group.split(" and ")) for group in requirement.split(" OR ")
        ]
        def supplied(path):
            if path == "internal_pca":
                return values.get("method") == "internal_pca"
            return present(value_at(values, path))

        if not any(all(supplied(path) for path in alternative) for alternative in alternatives):
            missing.append(requirement)
    return missing


def checked_request(workspace, body):
    validate_contract("RunRequest", body)
    if body["workspace_id"].lower() != str(workspace.pk):
        raise Http404
    if not body["question"].strip() or not body["idempotency_key"].strip():
        raise InvalidInput("The question and idempotency key must have content.")
    if len(body["idempotency_key"]) > 120 or len(body["question"]) > 1200:
        raise InvalidInput("The question or idempotency key is too long.")
    method = contracts.METHODS[(body["method_id"], body["method_version"])]
    if not method["quick"] and body.get("quick_id") is not None:
        raise InvalidInput({"quick_id": "Only quick methods have a quick tool ID."})

    refs = {}
    inspect_contract_values(workspace, body, refs)
    for ref in body["evidence_refs"]:
        if ref["kind"] != "evidence":
            raise InvalidInput({"evidence_refs": "Use evidence references."})

    inputs = body["input"]
    try:
        provenance.validate_observed(workspace, inputs)
    except ValueError as exc:
        raise InvalidInput(str(exc)) from None
    for path, binding in method.get("dataset_requirements", {}).items():
        value = value_at(inputs, path)
        if value is None:
            continue
        # Some typed inputs accept either inline rows or a reference.
        if isinstance(value, dict) and set(value) == {"kind", "id", "version"}:
            ref = refs[(value["kind"], value["id"], value["version"])]
            if isinstance(binding, list):
                if not isinstance(ref, models.Dataset) or ref.schema_id not in binding:
                    raise InvalidInput({path: "The referenced dataset must use a compatible schema."})
            elif value["kind"] != binding:
                raise InvalidInput({path: f"Expected a {binding} reference."})

    for pk in body["dependency_run_ids"]:
        get_object_or_404(models.AnalysisRun, workspace=workspace, pk=pk)
    if method["method_id"] == "S01.diagnose":
        check_metric_scope(workspace, inputs)
    if method["method_id"] == "M09.network":
        check_graph_endpoints(workspace, inputs)
    return method


def check_graph_endpoints(workspace, inputs):
    nodes_ref = value_at(inputs, "graph.nodes_ref")
    edges_ref = value_at(inputs, "graph.edges_ref")
    if nodes_ref is None or edges_ref is None:
        return
    nodes, edges = (resolve_ref(workspace, ref) for ref in (nodes_ref, edges_ref))
    node_keys = {row["node_key"] for row in nodes.payload["rows"]}
    if any(row["source_key"] not in node_keys or row["target_key"] not in node_keys
           for row in edges.payload["rows"]):
        raise InvalidInput({"graph.edges_ref": "An edge references a node absent from the selected node dataset."})


def check_metric_scope(workspace, inputs):
    actual, target = inputs.get("actual_value"), inputs.get("target_value")
    if actual and target and any(
        actual[field] != target[field] for field in ("metric_key", "unit", "currency", "scope")
    ):
        raise InvalidInput({"code": "METRIC_SCOPE_MISMATCH"})
    for item in (actual, target):
        if item and item["unit"] != item["scope"]["unit"]:
            raise InvalidInput({"code": "METRIC_SCOPE_MISMATCH"})
    if inputs.get("actual") and inputs.get("goal"):
        observation, goal = (resolve_ref(workspace, inputs[field]) for field in ("actual", "goal"))
        if observation.metric_id != goal.metric_id:
            raise InvalidInput({"code": "METRIC_SCOPE_MISMATCH"})
