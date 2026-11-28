"""Persistence and delivery of public, immutable analysis artifacts."""

from django.http import Http404

from . import contracts, models
from .api import inspect_contract_values, validate_contract


PUBLIC_TYPES = frozenset(
    option["properties"]["artifact_type"]["const"]
    for option in contracts.SCHEMA["$defs"]["ArtifactEnvelope"]["oneOf"]
) - {"Connection", "SyncRun", "WorkbenchPreferences"}


def envelope(row):
    result = {
        "artifact_id": str(row.pk), "artifact_type": row.artifact_type, "schema_version": row.schema_version,
        "version": row.version, "workspace_id": str(row.workspace_id), "payload": row.payload,
    }
    if row.artifact_type not in PUBLIC_TYPES or contracts.validate("ArtifactEnvelope", result):
        raise Http404
    validate_workspace_payload(row.workspace, result["payload"])
    return result


def store(run, items):
    for item in items:
        validate_contract("ArtifactEnvelope", item)
        if (
            item["artifact_type"] not in PUBLIC_TYPES
            or item["workspace_id"].lower() != str(run.workspace_id)
            or item["version"] != 1
        ):
            raise ValueError("Expected a first-version public artifact for this run's workspace.")
        payload = item["payload"]
        validate_workspace_payload(run.workspace, payload)
        models.Artifact.objects.create(
            id=item["artifact_id"], workspace_id=run.workspace_id, run=run,
            artifact_type=item["artifact_type"], schema_version=item["schema_version"], payload=payload,
        )


def validate_workspace_payload(workspace, payload):
    if "workspace_id" in payload and payload["workspace_id"].lower() != str(workspace.pk):
        raise Http404
    inspect_contract_values(workspace, payload)
