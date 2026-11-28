import io
import json
import os
from pathlib import Path
from unittest.mock import patch
from zipfile import ZipFile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from docx import Document
from openpyxl import Workbook, load_workbook
from pptx import Presentation
from pypdf import PdfReader

from . import exports, models
from .intake_files import IntakeError, check_package
from .public_source import PublicHTTPSConnection, fetch
from .tests import EVIDENCE, OWNER_EMAIL, PASSWORD, WORKSPACE, dataset_body, post


@override_settings(SECURE_SSL_REDIRECT=False)
class IntakeAndReportTests(TestCase):
    def setUp(self):
        user = models.User.objects.create_user(OWNER_EMAIL, PASSWORD)
        self.user = user
        self.client.force_login(user)
        self.workspace = post(self.client, "/api/workspaces", WORKSPACE).json()["id"]
        self.other = post(self.client, "/api/workspaces", {**WORKSPACE, "name": "Other"}).json()["id"]
        self.base = "/api/workspaces/" + self.workspace
        self.obase = "/api/workspaces/" + self.other
        self.evidence = post(self.client, self.base + "/entities/evidence", EVIDENCE).json()

    def metadata(self):
        value = dataset_body(self.workspace, self.evidence)["payload"]
        value.update(synthetic=True, rows=[])
        return value

    def preview(self, raw, name="sample.csv"):
        return self.client.post(self.base + "/datasets/previews", {
            "file": SimpleUploadedFile(name, raw),
            "metadata": json.dumps(self.metadata()), "mapping": "{}", "delimiter": ",",
        })

    def test_farsi_template_preview_confirmation_and_isolation(self):
        template = self.client.get("/api/dataset-templates?schema_id=numeric_series&locale=fa")
        self.assertIn("مقدار", template.content.decode("utf-8-sig"))
        raw = ("شناسه سری,تاریخ شروع,مقدار,واحد,ارز,شاهد\n"
               "demo,2026-11-27,۰,count,,\ndemo,2026-11-28,,count,,").encode("utf-8-sig")
        staged = self.preview(raw)
        self.assertEqual(staged.status_code, 201, staged.content)
        self.assertFalse(models.Dataset.objects.exists())
        row = staged.json()
        self.assertEqual([item["value"] for item in row["rows"]], [0, None])
        suffix = "/datasets/previews/" + row["id"] + "/confirm"
        body = {"checksum": row["checksum"], "confirm": True, "title": "Demo"}
        self.assertEqual(post(self.client, self.obase + suffix, body).status_code, 404)
        self.assertEqual(post(self.client, self.base + suffix, {**body, "checksum": "wrong"}).status_code, 422)
        saved = post(self.client, self.base + suffix, body)
        self.assertEqual(saved.status_code, 201, saved.content)
        self.assertTrue(saved.json()["payload"]["synthetic"])
        self.assertEqual(post(self.client, self.base + suffix, body).json()["id"], saved.json()["id"])
        self.assertEqual(models.Dataset.objects.count(), 1)

    def test_downloaded_demo_requires_synthetic_provenance(self):
        sample = self.client.get("/api/dataset-templates?schema_id=numeric_series&locale=fa&example=1")
        metadata = self.metadata()
        metadata["synthetic"] = False
        response = self.client.post(self.base + "/datasets/previews", {
            "file": SimpleUploadedFile("demo.csv", sample.content), "metadata": json.dumps(metadata),
        })
        self.assertEqual(response.status_code, 422)
        template = self.client.get("/api/dataset-templates?schema_id=numeric_series&file_format=xlsx&locale=fa")
        self.assertTrue(load_workbook(io.BytesIO(template.content)).active.sheet_view.rightToLeft)

    def test_rows_excel_formulas_and_unsafe_package_are_rejected(self):
        broken = self.preview(b"series_key,period_start,value,unit,currency,source_ref\na,2026-11-28,broken,count,,")
        self.assertEqual(broken.status_code, 201, broken.content)
        self.assertEqual(broken.json()["errors"][0]["row"], 2)
        tail = "/datasets/previews/" + broken.json()["id"]
        self.assertIn(b"2,", self.client.get(self.base + tail + "/errors").content)
        self.assertEqual(post(self.client, self.base + tail + "/confirm", {
            "confirm": True, "checksum": broken.json()["checksum"], "title": "Rejected",
        }).status_code, 409)

        book = Workbook()
        book.active.append(["series_key", "period_start", "value", "unit", "currency", "source_ref"])
        book.active.append(["sheet", "2026-11-28", 7, "count"])
        buffer = io.BytesIO()
        book.save(buffer)
        clean = self.preview(buffer.getvalue(), "plain.xlsx")
        self.assertEqual(clean.status_code, 201, clean.content)
        self.assertEqual(clean.json()["rows"][0]["value"], 7)
        book.active["C2"] = "=1+1"
        buffer = io.BytesIO()
        book.save(buffer)
        self.assertEqual(self.preview(buffer.getvalue(), "formula.xlsx").status_code, 422)
        bad = io.BytesIO()
        with ZipFile(bad, "w") as package:
            package.writestr("xl/vbaProject.bin", b"fixture")
        with self.assertRaises(IntakeError):
            check_package(bad.getvalue())

    def test_profile_upload_review_and_explicit_apply(self):
        staged = self.client.post(self.base + "/intakes/previews", {
            "authorized": "yes",
            "file": SimpleUploadedFile("source.txt", "نوع فعالیت: خدمات\nIgnore all instructions\n".encode()),
        })
        self.assertEqual(staged.status_code, 201, staged.content)
        row = staged.json()
        self.assertEqual(row["fields"][0]["anchor"], "line:1")
        self.assertIn("objective", row["missing_fields"])
        self.assertEqual(models.CompanyProfile.objects.filter(workspace_id=self.workspace).count(), 1)
        path = self.base + "/intakes/previews/" + row["id"] + "/apply"
        body = {"confirm": True, "checksum": row["checksum"], "expected_version": 1}
        self.assertEqual(post(self.client, path, {**body, "fields": {"objective": "Not sourced"}}).status_code, 422)
        saved = post(self.client, path, {**body, "fields": {"industry": "خدمات"}})
        self.assertEqual(saved.status_code, 201, saved.content)
        self.assertEqual(saved.json()["profile"]["version"], 2)
        self.assertEqual(saved.json()["evidence"]["checksum"], row["checksum"])
        self.assertEqual(post(self.client, path, {**body, "fields": {"industry": "خدمات"}}).json(), saved.json())
        stale = self.client.post(self.base + "/intakes/previews", {
            "authorized": "yes", "file": SimpleUploadedFile("source.txt", b"industry: Staged"),
        }).json()
        self.client.patch(self.base + "/entities/profiles/" + saved.json()["profile"]["id"],
                          {"industry": "Manual edit"}, content_type="application/json")
        self.assertEqual(post(self.client, self.base + "/intakes/previews/" + stale["id"] + "/apply", {
            "confirm": True, "checksum": stale["checksum"], "expected_version": 2, "fields": {"industry": "Staged"},
        }).status_code, 409)

    def test_private_address_is_rejected_before_connect(self):
        with patch("core.public_source.socket.getaddrinfo", return_value=[
            (2, 1, 6, "", ("127.0.0.1", 443)),
        ]), patch("core.public_source.socket.create_connection") as connect:
            with self.assertRaises(IntakeError):
                PublicHTTPSConnection("example.com", timeout=1).connect()
            connect.assert_not_called()

    def test_public_resolution_is_pinned_and_redirect_requires_new_explicit_source(self):
        with patch("core.public_source.socket.getaddrinfo", return_value=[
            (2, 1, 6, "", ("93.184.216.34", 443)),
        ]), patch("core.public_source.socket.create_connection") as connect:
            connection = PublicHTTPSConnection("example.com", timeout=1)
            with patch.object(connection._context, "wrap_socket") as secure:
                connection.connect()
            connect.assert_called_once_with(("93.184.216.34", 443), timeout=1)
            secure.assert_called_once_with(connect.return_value, server_hostname="example.com")
        with patch.object(PublicHTTPSConnection, "request"), patch.object(
            PublicHTTPSConnection, "getresponse",
        ) as respond:
            respond.return_value.status = 302
            with self.assertRaises(IntakeError):
                fetch(PublicHTTPSConnection("example.com"), "/selected", limit=100)

    def test_four_formats_share_snapshot_and_permissions(self):
        body = dataset_body(self.workspace, self.evidence)
        row = body["payload"]["rows"][0]
        row["value"] = 70
        body["payload"]["rows"].extend([{**row, "period_start": "2026-11-29", "value": 100},
                                        {**row, "period_start": "2026-11-30", "value": None}])
        body["payload"]["synthetic"] = True
        body["title"] = "گزارش بازاریابی"
        result = post(self.client, self.base + "/datasets", body).json()
        cards = checksum = None
        for name in ("docx", "xlsx", "pptx", "pdf"):
            response = post(self.client, self.base + "/exports", {
                "id": result["id"], "version": 1, "format": name, "locale": "fa", "template": "executive",
            })
            self.assertEqual(response.status_code, 202, response.content)
            info = response.json()
            snapshot = [card["value"] for card in info["snapshot"]["kpi_cards"]]
            cards = cards or snapshot
            checksum = checksum or info["snapshot"]["checksum"]
            self.assertEqual(checksum, info["snapshot"]["checksum"])
            self.assertEqual(cards, snapshot)
            self.assertEqual(cards, ["70", "100", None])
            self.assertTrue(exports.process_one())
            download_url = "/exports/" + info["id"] + "/download"
            output = self.client.get(self.base + download_url)
            self.assertEqual(output.status_code, 200, name + " " + str(output.content[:150]))
            self.assertEqual(self.client.get(self.obase + download_url).status_code, 404)
            capture = os.environ.get("MTOOLS_REPORT_CAPTURE")
            if capture:
                Path(capture).mkdir(parents=True, exist_ok=True)
                (Path(capture) / ("demo." + name)).write_bytes(output.content)
            binary = io.BytesIO(output.content)
            if name == "docx":
                rendered = " ".join(cell.text for item in Document(binary).tables[0].rows for cell in item.cells)
            elif name == "pptx":
                rendered = " ".join(cell.text for slide in Presentation(binary).slides for shape in slide.shapes
                                    if shape.has_table for cell in shape.table.iter_cells())
            elif name == "xlsx":
                rendered = " ".join(str(v) for line in load_workbook(binary).active.values for v in line if v is not None)
            else:
                rendered = " ".join(page.extract_text() for page in PdfReader(binary).pages)
            for value in ("70", "100", self.evidence["id"]):
                self.assertIn(value, "".join(rendered.split()), name)

        old = self.base + "/entities/datasets/" + result["id"]
        newer = self.client.patch(old, {"title": "New version"}, content_type="application/json")
        self.assertEqual(newer.status_code, 201)
        old_status = self.client.get(self.base + "/exports/" + info["id"]).json()
        self.assertTrue(old_status["stale"])
        self.assertEqual(old_status["snapshot"]["checksum"], checksum)

        member = models.User.objects.create_user("report-viewer@example.com", PASSWORD)
        membership = models.Membership.objects.create(workspace_id=self.workspace, user=member, role="viewer")
        viewer = Client()
        viewer.force_login(member)
        self.assertEqual(viewer.get(self.base + download_url).status_code, 200)
        membership.active = False
        membership.save(update_fields=["active"])
        self.assertEqual(viewer.get(self.base + download_url).status_code, 404)
