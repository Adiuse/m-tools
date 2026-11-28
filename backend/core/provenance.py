"""Evidence rules shared by analysis inputs, results, and report snapshots."""

from . import models
from .api import inspect_contract_values, resolve_ref


def observed_claims(value):
    if isinstance(value, dict):
        if value.get("kind") == "observed" and "statement" in value and "evidence_refs" in value:
            yield value["evidence_refs"]
        elif value.get("basis") == "observed" and "metric_key" in value and "source_ref" in value:
            yield [value["source_ref"]] if value["source_ref"] else []
        for item in value.values():
            yield from observed_claims(item)
    elif isinstance(value, list):
        for item in value:
            yield from observed_claims(item)


def has_synthetic_source(records):
    return any(
        (isinstance(record, models.Dataset) and record.payload["synthetic"])
        or (isinstance(record, models.Artifact) and record.artifact_type == "ReportViewModel"
            and record.payload.get("status") == "demo")
        for record in records
    )


def observed_source(workspace, ref):
    if ref["kind"] == "evidence":
        evidence = resolve_ref(workspace, ref)
        return evidence.kind != "assumption" and not evidence.claim_only
    if ref["kind"] == "observation":
        observation = resolve_ref(workspace, ref)
        return (observation.evidence.kind != "assumption" and not observation.evidence.claim_only
                and (observation.dataset is None or not observation.dataset.payload["synthetic"]))
    if ref["kind"] == "dataset":
        dataset = resolve_ref(workspace, ref)
        return (not dataset.payload["synthetic"] and dataset.evidence.kind != "assumption"
                and not dataset.evidence.claim_only)
    return False


def validate_observed(workspace, content, *, context=()):
    claims = list(observed_claims(content))
    if not claims:
        return
    refs = {}
    inspect_contract_values(workspace, [content, *context], refs)
    if has_synthetic_source(refs.values()):
        raise ValueError("Synthetic inputs cannot support observed results.")
    if any(not any(observed_source(workspace, ref) for ref in claim) for claim in claims):
        raise ValueError("Observed findings require authorized observational evidence.")
