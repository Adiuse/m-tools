import csv
import hashlib
import io
import json
import uuid
from datetime import timedelta
from pathlib import Path

from django.db import transaction
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from . import contracts, models
from .api import (Conflict, InvalidInput, audit, dataset_values, fields, validate_dataset_row,
                  workspace_access, workspace_entities)
from .intake_files import IntakeError, MAX_COLUMNS, MAX_ROWS, normalize_cell, read_upload, rows_from_file

DEMO_MARK = "# M-Tools synthetic example"

LABELS_FA = {
    "series_key": "شناسه سری", "period_start": "تاریخ شروع", "value": "مقدار",
    "unit": "واحد", "currency": "ارز", "source_ref": "شاهد",
}


def row_types():
    return {key[4:]: schema for key, schema in contracts.SCHEMA["$defs"].items() if key.startswith("Row_")}


@api_view(["GET"])
def examples(request, tool_id):
    methods = [method for method in contracts.CATALOG if method["tool_id"] == tool_id]
    if not methods:
        raise Http404
    results = []
    for method in methods:
        ids = {schema for binding in method.get("dataset_requirements", {}).values()
               if isinstance(binding, list) for schema in binding}
        available = "numeric_series" in ids
        results.append({
            "method_id": method["method_id"], "method_version": method["method_version"],
            "status": "synthetic_fixture" if available else "planned",
            "schema_id": "numeric_series" if available else None,
            "url": f"/api/tools/{tool_id}/templates?method_id={method['method_id']}&schema_id=numeric_series&example=1"
                   if available else None,
        })
    return Response(results)


@api_view(["GET"])
def templates(request, tool_id=None):
    schemas = row_types()
    if tool_id is not None:
        methods = [row for row in contracts.CATALOG if row["tool_id"] == tool_id
                   and request.query_params.get("method_id", row["method_id"]) == row["method_id"]]
        if not methods:
            raise Http404
        method_schemas = {schema for method in methods for binding in method.get("dataset_requirements", {}).values()
                          if isinstance(binding, list) for schema in binding}
        schemas = {key: value for key, value in schemas.items() if key in method_schemas}
    chosen = request.query_params.get("schema_id")
    if chosen is None:
        return Response([{"schema_id": key, "version": 1, "columns": list(schema["properties"]),
                          "required": schema["required"]} for key, schema in schemas.items()])
    if chosen not in schemas:
        raise Http404
    properties = schemas[chosen]["properties"]
    localized = request.query_params.get("locale") == "fa"
    labels = [LABELS_FA.get(key, key) if localized else key for key in properties]
    output = [labels]
    if request.query_params.get("example") == "1":
        if chosen != "numeric_series":
            raise Http404
        output = [[DEMO_MARK], labels, ["demo", "2026-01-01", 70, "count", "", ""],
                  ["demo", "2026-01-02", 100, "count", "", ""],
                  ["demo", "2026-01-03", "", "count", "", ""]]
    if request.query_params.get("file_format") == "xlsx":
        import xlsxwriter
        binary = io.BytesIO()
        workbook = xlsxwriter.Workbook(binary, {"in_memory": True, "strings_to_formulas": False})
        sheet = workbook.add_worksheet("Dataset")
        if localized:
            sheet.right_to_left()
        for index, row in enumerate(output):
            sheet.write_row(index, 0, row)
        workbook.close()
        return HttpResponse(binary.getvalue(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            headers={"Content-Disposition": f'attachment; filename="{chosen}-v1.xlsx"'})
    out = io.StringIO()
    csv.writer(out).writerows(output)
    return HttpResponse(out.getvalue().encode("utf-8-sig"), content_type="text/csv; charset=utf-8",
                        headers={"Content-Disposition": f'attachment; filename="{chosen}-v1.csv"'})


def parse_rows(workspace, raw, extension, spec, metadata, mapping, sheet, delimiter):
    schema_id = metadata["schema_id"]
    rows = iter(rows_from_file(raw, extension, sheet=sheet, delimiter=delimiter))
    header = [str(cell or "").strip() for cell in next(rows, [])]
    start = 2
    if header == [DEMO_MARK]:
        if metadata.get("synthetic") is not True:
            raise IntakeError("Mark the sample as synthetic before importing it.")
        header = [str(cell or "").strip() for cell in next(rows, [])]
        start = 3
    if not header or not all(header) or len(header) > MAX_COLUMNS or len(set(header)) != len(header):
        raise IntakeError("Use a unique, nonempty header row.")
    aliases = {label: key for key, label in LABELS_FA.items()}
    mapped = [mapping.get(key, aliases.get(key, key)) for key in header]
    properties = spec["properties"]
    if any(key not in properties for key in mapped) or len(set(mapped)) != len(mapped):
        raise IntakeError("Map each column to a distinct schema field.")
    accepted, errors, seen, refs = [], [], {}, {}
    timezone_name = metadata["scope"]["period"]["timezone"]
    for index, row in enumerate(rows, start):
        if index - start >= MAX_ROWS:
            raise IntakeError("The file has too many rows.")
        if not any(value is not None and value != "" for value in row):
            continue
        try:
            if len(row) > len(header):
                raise IntakeError("The row has extra cells.")
            by_key = dict(zip(mapped, row))
            normalized = {}
            for key, column in properties.items():
                if key in by_key or key in spec["required"]:
                    normalized[key] = normalize_cell(by_key.get(key), column, timezone_name)
            if "source_ref" in normalized and normalized["source_ref"] is None:
                normalized["source_ref"] = metadata["source_ref"]
            issue = contracts.validate("Row_" + schema_id, normalized)
            if issue is not None:
                field = ".".join(map(str, issue.absolute_path)) or "row"
                raise IntakeError(f"Invalid or missing value in {field}.")
            validate_dataset_row(workspace, metadata, normalized, seen, refs)
            accepted.append(normalized)
        except Http404:
            errors.append({"row": index, "reason": "A versioned reference is unavailable in this workspace."})
        except InvalidInput as exc:
            errors.append({"row": index, "reason": str(exc.detail)})
        except (ValueError, TypeError) as exc:
            reason = str(exc) if isinstance(exc, IntakeError) else "Use a typed value for the selected column."
            errors.append({"row": index, "reason": reason})
    return accepted, errors


@api_view(["POST"])
@parser_classes([MultiPartParser])
def preview(request, workspace_id):
    workspace, role = workspace_access(request, workspace_id)
    if role == "viewer":
        raise PermissionDenied()
    try:
        metadata = json.loads(request.data.get("metadata", "{}"))
        mapping = json.loads(request.data.get("mapping", "{}"))
        if (not isinstance(metadata, dict) or not isinstance(mapping, dict)
                or not all(isinstance(value, str) for value in mapping.values())):
            raise IntakeError("Use valid metadata and column mapping.")
        schema_id = metadata.get("schema_id")
        if schema_id not in row_types() or "source_ref" not in metadata:
            raise IntakeError("Select a registered schema and source evidence.")
        upload = request.FILES.get("file")
        raw = read_upload(upload)
        checksum = hashlib.sha256(raw).hexdigest()
        if ("schema_version" in metadata and (type(metadata["schema_version"]) is not int or metadata["schema_version"] != 1)
                or request.data.get("template_version", "1") != "1"):
            raise IntakeError("Download the current version of the template.")
        if "workspace_id" in metadata and metadata["workspace_id"] != str(workspace.pk):
            raise Http404
        metadata.update(workspace_id=str(workspace.pk), schema_version=1, rows=[])
        dataset_values(workspace, metadata)
        rows, errors = parse_rows(workspace, raw, Path(upload.name).suffix.lower(), row_types()[schema_id],
                                  metadata, mapping, request.data.get("sheet"), request.data.get("delimiter", ","))
        metadata["rows"] = rows
    except (ValueError, TypeError) as exc:
        raise InvalidInput(str(exc)) from None
    row = models.IntakePreview.objects.create(
        workspace=workspace, creator=request.user, kind="dataset", checksum=checksum,
        payload={"document": metadata, "errors": errors, "mapping": mapping, "file_name": upload.name},
        expires_at=timezone.now() + timedelta(hours=1),
    )
    return Response({"id": row.pk, "checksum": checksum, "template_version": 1, "mapping": mapping,
                     "accepted": len(rows), "errors": errors,
                     "rows": rows[:20], "synthetic": metadata["synthetic"]}, status=201)


def get_preview(workspace, user, pk, kind):
    return get_object_or_404(models.IntakePreview, workspace=workspace, creator=user, kind=kind,
                             expires_at__gt=timezone.now(), pk=pk)


@api_view(["GET"])
def errors(request, workspace_id, pk):
    workspace, _ = workspace_access(request, workspace_id)
    preview_row = get_preview(workspace, request.user, pk, "dataset")
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(["row", "reason"])
    writer.writerows((error["row"], error["reason"]) for error in preview_row.payload["errors"])
    return HttpResponse(out.getvalue(), content_type="text/csv; charset=utf-8",
                        headers={"Content-Disposition": 'attachment; filename="validation-errors.csv"'})


@api_view(["GET", "POST"])
@transaction.atomic
def datasets(request, workspace_id):
    workspace, _ = workspace_access(request, workspace_id, write=request.method == "POST")
    body = request.data
    if request.method == "POST" and isinstance(body, dict) and "preview_id" in body:
        try:
            pk = uuid.UUID(body["preview_id"])
        except (ValueError, TypeError, AttributeError):
            raise InvalidInput({"preview_id": "Use a staged preview UUID."}) from None
        if set(body) != {"preview_id", "confirm", "checksum", "title", "mapping", "template_version"}:
            raise InvalidInput("Confirm the exact mapping and template version from the preview.")
        return confirm_preview(request, workspace, pk, {key: value for key, value in body.items() if key != "preview_id"})
    return workspace_entities(request, workspace, "datasets")


@api_view(["POST"])
@transaction.atomic
def confirm(request, workspace_id, pk):
    workspace, _ = workspace_access(request, workspace_id, write=True)
    return confirm_preview(request, workspace, pk, request.data)


def confirm_preview(request, workspace, pk, body):
    row = get_preview(workspace, request.user, pk, "dataset")
    if (not isinstance(body, dict) or set(body) not in ({"confirm", "checksum", "title"},
                                                       {"confirm", "checksum", "title", "template_version", "mapping"})
            or body["confirm"] is not True or body["checksum"] != row.checksum):
        raise InvalidInput("Confirm the staged checksum explicitly.")
    if "template_version" in body and (
        type(body["template_version"]) is not int or body["template_version"] != 1 or body["mapping"] != row.payload["mapping"]
    ):
        raise Conflict("The confirmed mapping or template version differs from the preview.")
    title = body.get("title")
    if not isinstance(title, str) or not title.strip() or len(title) > 200:
        raise InvalidInput("Enter a dataset title of up to 200 characters.")
    title = title.strip()
    from .api import inspect_contract_values
    inspect_contract_values(workspace, title)
    if row.applied_id:
        existing = get_object_or_404(models.Dataset, workspace=workspace, pk=row.applied_id)
        if existing.title != title.strip():
            raise Conflict()
        return Response(fields(existing))
    if row.payload["errors"] or not row.payload["document"]["rows"]:
        raise Conflict("Review the row errors and stage a corrected file.")
    document = row.payload["document"]
    record = models.Dataset.objects.create(
        workspace=workspace, created_by=request.user, title=title.strip(), payload=document,
        **dataset_values(workspace, document),
    )
    row.applied_id = record.pk
    row.save(update_fields=["applied_id"])
    audit(request, workspace, "datasets_imported", record)
    return Response(fields(record), status=201)
