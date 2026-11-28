import json
import uuid
from datetime import timedelta
from urllib.parse import parse_qs, urlsplit

from django.core import mail
from django.db import IntegrityError, transaction
from django.test import Client, TestCase, override_settings
from django.utils import timezone

from . import jobs, models
from .analysis import input_hash


OWNER_EMAIL = "owner@example.com"
PASSWORD = "Trade research 824! dev"
WORKSPACE = {
    "name": "North market", "currency": "EUR", "timezone": "Europe/Berlin",
    "industry": "Retail", "offering": "Footwear", "objective": "Measure monthly demand",
}
EVIDENCE = {"kind": "internal", "title": "Count sheet", "collected_at": "2026-11-28", "quality_notes": "Checked"}


def post(client, url, data, **headers):
    return client.post(url, data=json.dumps(data), content_type="application/json", **headers)


def dataset_body(workspace, evidence):
    ref = {"kind": "evidence", "id": str(evidence["id"]), "version": evidence["version"]}
    return {"title": "Demand", "payload": {
        "schema_id": "numeric_series", "schema_version": 1, "workspace_id": str(workspace),
        "scope": {"population": "Retail", "grain": "day", "cohort": None, "unit": "count",
                  "period": {"start": "2026-11-01", "end_exclusive": "2026-12-01", "timezone": "Europe/Berlin"}},
        "source_ref": ref, "synthetic": False, "rows": [
            {"series_key": "walk-ins", "period_start": "2026-11-28", "value": 0,
             "unit": "count", "currency": None, "source_ref": ref},
        ], "columns": [], "coverage": "partial",
    }}


@override_settings(SECURE_SSL_REDIRECT=False, PUBLIC_ORIGIN="https://workbench.example")
class AccountTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)

    def csrf(self):
        self.client.get("/api/me")
        return {"HTTP_X_CSRFTOKEN": self.client.cookies["csrftoken"].value}

    def test_protected_login_and_private_session(self):
        models.User.objects.create_user(OWNER_EMAIL, PASSWORD)
        self.assertEqual(self.client.get("/api/workspaces").status_code, 401)
        credentials = {"email": OWNER_EMAIL.upper(), "password": PASSWORD}
        self.assertEqual(post(self.client, "/api/auth/login", credentials).status_code, 403)
        self.assertEqual(post(self.client, "/api/auth/login", credentials, **self.csrf()).status_code, 200)
        self.assertIn("no-store", self.client.get("/api/me").headers["Cache-Control"])
        self.assertEqual(post(self.client, "/api/workspaces", WORKSPACE).status_code, 403)
        self.assertEqual(post(self.client, "/api/workspaces", WORKSPACE, **self.csrf()).status_code, 201)
        self.assertEqual(post(self.client, "/api/auth/logout", {}, **self.csrf()).status_code, 200)
        self.assertEqual(self.client.get("/api/workspaces").status_code, 401)

    def test_activation_reset_and_single_use_tokens(self):
        for step, mode in (("register", "activate"), ("reset", "reset")):
            response = post(self.client, "/api/auth/" + step, {"email": OWNER_EMAIL}, **self.csrf())
            self.assertEqual(response.status_code, 202)
            parsed = urlsplit(mail.outbox[-1].body)
            self.assertEqual(parsed.query, "")
            params = {key: values[0] for key, values in parse_qs(parsed.fragment).items()}
            self.assertEqual(params["mode"], mode)
            user = models.User.objects.get(email=OWNER_EMAIL)
            self.assertEqual(user.is_active, mode == "reset")
            payload = {**params, "password": PASSWORD + mode}
            self.assertEqual(post(self.client, "/api/auth/password", payload, **self.csrf()).status_code, 200)
            self.assertEqual(post(self.client, "/api/auth/password", payload, **self.csrf()).status_code, 422)
        self.assertEqual(post(self.client, "/api/auth/login", {"email": OWNER_EMAIL, "password": PASSWORD + "reset"},
                              **self.csrf()).status_code, 200)


@override_settings(SECURE_SSL_REDIRECT=False)
class WorkspaceTests(TestCase):
    def setUp(self):
        self.owner = models.User.objects.create_user(OWNER_EMAIL, PASSWORD)
        self.observer = models.User.objects.create_user("viewer@example.com", PASSWORD)
        self.client.force_login(self.owner)
        self.one = post(self.client, "/api/workspaces", WORKSPACE).json()["id"]
        self.two = post(self.client, "/api/workspaces", {**WORKSPACE, "name": "South"}).json()["id"]
        self.root = "/api/workspaces/" + self.one
        self.other = "/api/workspaces/" + self.two
        self.evidence = post(self.client, self.root + "/entities/evidence", EVIDENCE).json()

    def test_workspace_creation_is_atomic(self):
        from unittest.mock import patch

        with patch("core.models.CompanyProfile.objects.create", side_effect=RuntimeError("profile failure")):
            with self.assertRaises(RuntimeError):
                post(self.client, "/api/workspaces", {**WORKSPACE, "name": "Interrupted"})
        self.assertFalse(models.Workspace.objects.filter(name="Interrupted").exists())
        self.assertEqual(models.Workspace.objects.count(), 2)
        self.assertEqual(models.Membership.objects.count(), 2)

    def test_manual_records_versions_and_scope(self):
        self.assertEqual(self.client.get(self.other + "/entities/evidence").json(), [])
        evid_url = self.root + "/entities/evidence/" + self.evidence["id"]
        revision = self.client.patch(evid_url, {"title": "Checked again"}, content_type="application/json")
        self.assertEqual(revision.status_code, 201, revision.content)
        self.assertEqual(revision.json()["version"], 2)
        self.assertEqual(revision.json()["quality_notes"], "Checked")
        self.assertEqual(self.client.get(evid_url).json()["title"], "Count sheet")
        self.assertEqual(self.client.patch(evid_url, {"title": "Stale"}, content_type="application/json").status_code, 409)
        data = dataset_body(self.one, self.evidence)
        response = post(self.client, self.root + "/datasets", data)
        self.assertEqual(response.status_code, 201, response.content)
        self.assertEqual(response.json()["payload"]["rows"][0]["value"], 0)
        self.assertEqual(post(self.client, self.other + "/datasets", dataset_body(self.two, self.evidence)).status_code, 404)
        self.assertEqual(post(self.client, self.root + "/datasets", {**data, "bogus": 1}).status_code, 422)
        data["payload"]["rows"] *= 2
        self.assertEqual(post(self.client, self.root + "/datasets", data).status_code, 422)
        self.assertEqual(len(self.client.get(self.root + "/history").json()), 4)

    def test_judgment_entities_and_decimal_validation(self):
        metric = post(self.client, self.root + "/entities/metrics", {
            "key": "visits", "definition": "Daily visits", "unit": "count", "grain": "day", "direction": "increase",
        }).json()
        input_data = {"metric_id": metric["id"], "evidence_id": self.evidence["id"],
                      "period_start": "2026-11-27", "period_end": "2026-11-28", "value": "0"}
        observations = self.root + "/entities/observations"
        self.assertEqual(post(self.client, observations, {**input_data, "value": "0.5"}).status_code, 422)
        baseline = post(self.client, observations, input_data)
        self.assertEqual(baseline.status_code, 201, baseline.content)
        self.assertEqual(baseline.json()["value"], "0")
        self.assertEqual(post(self.client, observations, input_data).status_code, 409)
        self.assertEqual(post(self.client, self.root + "/entities/goals", {
            "metric_id": metric["id"], "baseline_id": baseline.json()["id"], "target": "15", "deadline": "2027-01-05",
        }).status_code, 201)
        self.assertEqual(post(self.client, self.root + "/entities/hypotheses", {
            "statement": "Demand increased after the display change.", "evidence_id": self.evidence["id"],
        }).status_code, 201)

    def test_membership_revocation_and_private_artifacts(self):
        other = Client()
        other.force_login(self.observer)
        self.assertEqual(other.get("/api/workspaces").json(), [])
        self.assertEqual(other.get(self.root + "/history").status_code, 404)
        self.assertEqual(post(self.client, self.root + "/memberships", {
            "email": self.observer.email, "role": "viewer",
        }).status_code, 200)
        self.assertEqual(len(other.get("/api/workspaces").json()), 1)
        self.assertEqual(other.get(self.root + "/entities/evidence").status_code, 200)
        self.assertEqual(post(other, self.root + "/entities/evidence", EVIDENCE).status_code, 403)
        self.assertEqual(other.get(self.root + "/memberships").status_code, 403)
        run = models.AnalysisRun.objects.create(
            workspace_id=self.one, creator=self.owner, tool_id="S01", method_id="S01.diagnose",
            method_version=1, idempotency_key="artifact", input_snapshot={}, input_hash="0" * 64,
        )
        artifact = models.Artifact.objects.create(
            workspace_id=self.one, run=run, artifact_type="ReportViewModel", schema_version=1, payload={},
        )
        suffix = "/artifacts/" + str(artifact.pk)
        self.assertEqual(other.get(self.root + suffix).status_code, 200)
        self.assertEqual(self.client.get(self.other + suffix).status_code, 404)
        self.assertEqual(post(self.client, self.root + "/memberships", {
            "email": self.observer.email, "role": "viewer", "active": False,
        }).status_code, 200)
        self.assertEqual(other.get(self.root + suffix).status_code, 404)
        self.assertEqual(other.get(self.root + "/history").status_code, 404)

    def test_compound_foreign_keys_and_db_immutability(self):
        row = models.Evidence.objects.get(pk=self.evidence["id"])
        with self.assertRaises(IntegrityError), transaction.atomic():
            models.Dataset.objects.create(
                workspace_id=self.two, evidence=row, title="Wrong workspace", schema_id="numeric_series",
                schema_version=1, payload={}, checksum="1" * 64, row_count=0, created_by=self.owner,
            )
        with self.assertRaises(IntegrityError), transaction.atomic():
            models.Evidence.objects.filter(pk=row.pk).update(title="Changed in place")
        self.assertEqual(models.Evidence.objects.get(pk=row.pk).title, EVIDENCE["title"])

    def run_body(self):
        return {
            "tool_id": "S01", "method_id": "S01.diagnose", "method_version": 1, "workspace_id": self.one,
            "question": "Why did demand fall?", "input": {}, "evidence_refs": [],
            "dependency_run_ids": [], "idempotency_key": "draft-one",
        }

    def test_catalog_preflight_draft_replay_and_scratch(self):
        catalog = self.client.get("/api/tools").json()
        self.assertEqual(len(catalog), 72)
        self.assertEqual(len({e["method_id"] for e in catalog if e["quick"]}), 15)
        self.assertEqual(len({e["tool_id"] for e in catalog if not e["quick"]}), 29)
        self.assertEqual({e["availability"] for e in catalog}, {"planned"})
        body = self.run_body()
        self.assertEqual(post(self.client, self.root + "/preflight", body).json()["availability"], "planned")
        self.assertEqual(post(self.client, self.root + "/runs", body).status_code, 503)
        created = post(self.client, self.root + "/drafts", body)
        self.assertEqual(created.status_code, 201, created.content)
        self.assertEqual(post(self.client, self.root + "/drafts", body).json()["id"], created.json()["id"])
        self.assertEqual(post(self.client, self.root + "/drafts", {**body, "question": "Different"}).status_code, 409)
        saved = self.client.patch(self.root + "/drafts/" + created.json()["id"],
                                  {**body, "idempotency_key": "revision", "question": "Updated"},
                                  content_type="application/json")
        self.assertEqual(saved.status_code, 201)
        self.assertEqual(saved.json()["version"], 2)
        ref = {"kind": "evidence", "id": self.evidence["id"], "version": 1}
        self.assertEqual(post(self.client, self.other + "/preflight", {
            **body, "workspace_id": self.two, "evidence_refs": [ref],
        }).status_code, 404)
        unassigned = Client()
        unassigned.force_login(self.observer)
        self.assertEqual(post(unassigned, "/api/scratch", {"quick_id": "QT01", "method_version": 1, "input": {}}).status_code, 503)
        self.assertEqual(post(unassigned, "/api/scratch", {"quick_id": "QT01", "method_version": 1,
                                                          "input": {}, "workspace_id": self.one}).status_code, 422)
        self.assertEqual(models.RunDraft.objects.count(), 2)
        self.assertFalse(models.AnalysisRun.objects.exists())
        self.assertFalse(models.Job.objects.exists())

    def queue(self):
        body = {**self.run_body(), "idempotency_key": "test-job"}
        run = models.AnalysisRun.objects.create(
            workspace_id=self.one, creator=self.owner, tool_id=body["tool_id"], method_id=body["method_id"],
            method_version=1, idempotency_key="test-job", input_snapshot=body, input_hash=input_hash(body),
        )
        return run, models.Job.objects.create(run=run, workspace_id=self.one, available_at=timezone.now())

    def test_leases_retry_and_atomic_result(self):
        run, job = self.queue()
        path = self.root + "/runs"
        self.assertEqual(post(self.client, path, run.input_snapshot).json()["run_id"], str(run.pk))
        self.assertEqual(post(self.client, path, {**run.input_snapshot, "question": "Another"}).status_code, 409)
        self.assertEqual(models.Job.objects.count(), 1)
        first = jobs.claim()
        self.assertEqual(first.pk, job.pk)
        self.assertIsNone(jobs.claim())
        jobs.retry(job.pk, first.lease_token, temporary=True)
        self.assertIsNone(jobs.claim())
        models.Job.objects.filter(pk=job.pk).update(available_at=timezone.now() - timedelta(seconds=1))
        second = jobs.claim()
        self.assertEqual(second.attempts, 2)
        with self.assertRaises(jobs.LeaseLost):
            jobs.retry(job.pk, first.lease_token, temporary=False)
        result = jobs.public_result(second.run)
        result.update(status="succeeded", analysis_status="needs_data")
        unbacked = {"kind": "observed", "statement": "Demand fell.", "value": None,
                    "evidence_refs": [], "assumption_refs": []}
        with self.assertRaises(ValueError):
            jobs.finish(job.pk, second.lease_token, {**result, "findings": [unbacked]})
        run.refresh_from_db()
        self.assertEqual(run.status, "running")
        self.assertIsNone(run.result)
        jobs.finish(job.pk, second.lease_token, result)
        run.refresh_from_db()
        self.assertEqual(run.result, result)
        self.assertFalse(models.Job.objects.exists())
        with self.assertRaises(IntegrityError), transaction.atomic():
            models.AnalysisRun.objects.filter(pk=run.pk).update(result={})

    def test_expired_lease_exhaustion(self):
        run, job = self.queue()
        models.Job.objects.filter(pk=job.pk).update(
            attempts=jobs.MAX_ATTEMPTS, lease_token=uuid.uuid4(), lease_until=timezone.now() - timedelta(seconds=1),
        )
        self.assertIsNone(jobs.claim())
        run.refresh_from_db()
        self.assertEqual(run.result["error_code"], "lease_exhausted")
        self.assertFalse(models.Job.objects.exists())

    def test_human_decision_approval_is_separate(self):
        run, job = self.queue()
        lease = jobs.claim()
        result = jobs.public_result(lease.run)
        result.update(status="succeeded", analysis_status="conditional", options=[
            {"id": "review", "title": "Review", "rationale": "Inspect sources",
             "cost": None, "evidence_refs": [], "risks": [], "violations": []},
        ])
        jobs.finish(job.pk, lease.lease_token, result)
        draft = post(self.client, self.root + "/decisions",
                     {"run_id": str(run.pk), "selected_option": "review", "reason": "Verify demand evidence"})
        self.assertEqual(draft.status_code, 201, draft.content)
        self.assertEqual(draft.json()["state"], "draft")
        approve = self.root + "/decisions/" + draft.json()["id"] + "/approve"
        models.Membership.objects.create(workspace_id=self.one, user=self.observer, role="editor")
        editor = Client()
        editor.force_login(self.observer)
        self.assertEqual(post(editor, approve, {}).status_code, 403)
        self.assertEqual(post(self.client, approve, {"approved_by": str(self.observer.pk)}).status_code, 422)
        self.assertEqual(post(self.client, approve, {}).json()["state"], "approved")
