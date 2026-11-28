"""Database leases for future registered analysis handlers."""

import uuid
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from . import contracts, models


MAX_ATTEMPTS = 3
LEASE_DURATION = timedelta(minutes=2)


class LeaseLost(Exception):
    pass


def public_result(run):
    if run.result is not None:
        return run.result
    return {
        "run_id": str(run.pk), "workspace_id": str(run.workspace_id), "tool_id": run.tool_id,
        "method_id": run.method_id, "method_version": run.method_version, "status": run.status,
        "analysis_status": None, "input_hash": run.input_hash, "findings": [], "options": [],
        "assumptions": [], "evidence_refs": run.input_snapshot["evidence_refs"], "limitations": [],
        "missing_fields": [], "output": None, "next_action": None, "error_code": None,
    }


def failed(job, error_code):
    result = public_result(job.run)
    result.update(status="failed", analysis_status="error", error_code=error_code)
    job.run.status, job.run.result = "failed", result
    job.run.save(update_fields=["status", "result"])
    job.delete()


@transaction.atomic
def claim():
    from django.db.models import Q

    now = timezone.now()
    candidates = models.Job.objects.select_for_update(skip_locked=True, of=("self",)).select_related("run")
    candidates = candidates.filter(available_at__lte=now).filter(
        Q(lease_until__isnull=True) | Q(lease_until__lte=now),
    ).order_by("available_at", "id")
    for job in candidates[:20]:
        if job.attempts >= MAX_ATTEMPTS:
            failed(job, "lease_exhausted")
            continue
        job.attempts += 1
        job.lease_token, job.lease_until = uuid.uuid4(), now + LEASE_DURATION
        job.save(update_fields=["attempts", "lease_token", "lease_until"])
        job.run.status = "running"
        job.run.save(update_fields=["status"])
        return job
    return None


def locked_lease(job_id, token):
    job = models.Job.objects.select_for_update(of=("self",)).select_related("run", "workspace").filter(
        pk=job_id, lease_token=token,
    ).first()
    if job is None or job.lease_until is None or job.lease_until <= timezone.now():
        raise LeaseLost()
    return job


@transaction.atomic
def retry(job_id, token, *, temporary):
    job = locked_lease(job_id, token)
    if not temporary or job.attempts >= MAX_ATTEMPTS:
        failed(job, "processing_failed")
        return
    job.available_at = timezone.now() + timedelta(seconds=2 ** job.attempts)
    job.lease_token = job.lease_until = None
    job.save(update_fields=["available_at", "lease_token", "lease_until"])
    job.run.status = "queued"
    job.run.save(update_fields=["status"])


@transaction.atomic
def finish(job_id, token, result, *, artifact_envelopes=()):
    from . import artifacts
    from .api import inspect_contract_values, resolve_ref

    job = locked_lease(job_id, token)
    artifact_envelopes = tuple(artifact_envelopes)
    template = public_result(job.run)
    identity = ("run_id", "workspace_id", "tool_id", "method_id", "method_version", "input_hash")
    if contracts.validate("RunResult", result) or any(result[key] != template[key] for key in identity):
        raise ValueError("Invalid run result or identity.")
    if result["status"] != "succeeded" or result["analysis_status"] not in ("ready", "conditional", "needs_data"):
        raise ValueError("A completed result requires a valid analysis status.")
    if result["analysis_status"] == "ready" and result["output"] is None:
        raise ValueError("Ready results require a method output.")
    inspect_contract_values(job.workspace, result)
    artifacts.store(job.run, artifact_envelopes)
    values = [result, *(item["payload"] for item in artifact_envelopes)]
    for finding in observed_claims(values):
        if finding["kind"] == "observed" and not any(
            valid_observed_source(job.workspace, ref, resolve_ref)
            for ref in finding["evidence_refs"]
        ):
            raise ValueError("Observed findings require authorized evidence.")
    job.run.status, job.run.result = "succeeded", result
    job.run.save(update_fields=["status", "result"])
    job.delete()


def observed_claims(value):
    if isinstance(value, dict):
        if value.get("kind") == "observed" and "statement" in value and "evidence_refs" in value:
            yield value
        elif value.get("basis") == "observed" and "metric_key" in value and "source_ref" in value:
            yield {"kind": "observed", "evidence_refs": [value["source_ref"]] if value["source_ref"] else []}
        for item in value.values():
            yield from observed_claims(item)
    elif isinstance(value, list):
        for item in value:
            yield from observed_claims(item)


def valid_observed_source(workspace, ref, resolve_ref):
    if ref["kind"] == "evidence":
        return resolve_ref(workspace, ref).kind != "assumption"
    if ref["kind"] == "observation":
        return resolve_ref(workspace, ref).evidence.kind != "assumption"
    if ref["kind"] == "dataset":
        return not resolve_ref(workspace, ref).payload["synthetic"]
    return False
