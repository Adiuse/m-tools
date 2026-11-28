"""Bounded, read-only parsing for approved intake formats."""

import csv
import io
import json
import re
from datetime import date, datetime, timezone
from pathlib import PurePosixPath
from zipfile import BadZipFile, ZipFile
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from defusedxml.ElementTree import fromstring
from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException

MAX_BYTES = 2_000_000
MAX_ROWS = 2000
MAX_COLUMNS = 64
NUMBER = re.compile(r"-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?")
FORMULA = re.compile(r"^[\s]*[=+@]|^[\s]*-(?![0-9])")
DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩٫", "01234567890123456789.")


class IntakeError(ValueError):
    pass


def read_upload(upload):
    if upload is None or upload.size > MAX_BYTES:
        raise IntakeError("Select a file up to 2 MB.")
    result = upload.read(MAX_BYTES + 1)
    if len(result) > MAX_BYTES:
        raise IntakeError("Select a file up to 2 MB.")
    return result


def check_package(raw):
    try:
        with ZipFile(io.BytesIO(raw)) as file:
            entries = file.infolist()
            if len(entries) > 400 or sum(item.file_size for item in entries) > 16_000_000:
                raise IntakeError("The Office package exceeds expanded size limits.")
            for entry in entries:
                path = PurePosixPath(entry.filename)
                lower = entry.filename.lower()
                if path.is_absolute() or ".." in path.parts or "\\" in entry.filename or entry.flag_bits & 1:
                    raise IntakeError("Unsafe Office package.")
                if any(token in lower for token in ("vbaproject", "macrosheet", "/externallinks/", "/embeddings/")):
                    raise IntakeError("Macros, external links and embedded files are not accepted.")
                if lower.endswith(".rels"):
                    for relation in fromstring(file.read(entry)):
                        if relation.get("TargetMode", "").lower() == "external":
                            raise IntakeError("External Office relationships are not accepted.")
    except (BadZipFile, ValueError, OSError, SyntaxError) as exc:
        if isinstance(exc, IntakeError):
            raise
        raise IntakeError("Invalid Office package.") from exc


def rows_from_file(raw, extension, *, sheet=None, delimiter=","):
    if extension == ".csv":
        if delimiter not in (",", ";", "\t"):
            raise IntakeError("Choose comma, semicolon or tab as the delimiter.")
        try:
            yield from csv.reader(io.StringIO(raw.decode("utf-8-sig")), delimiter=delimiter, strict=True)
        except (UnicodeError, csv.Error) as exc:
            raise IntakeError("Use a valid UTF-8 CSV.") from exc
    elif extension == ".xlsx":
        check_package(raw)
        try:
            book = load_workbook(io.BytesIO(raw), read_only=True, data_only=False, keep_links=False)
        except (BadZipFile, InvalidFileException, ValueError, OSError, KeyError, SyntaxError) as exc:
            raise IntakeError("Invalid XLSX workbook.") from exc
        try:
            if not book.sheetnames:
                raise IntakeError("The workbook has no worksheets.")
            name = sheet or book.sheetnames[0]
            if name not in book.sheetnames:
                raise IntakeError("The selected sheet does not exist.")
            grid = book[name]
            if (grid.max_column or 0) > MAX_COLUMNS or (grid.max_row or 0) > MAX_ROWS + 2:
                raise IntakeError("The selected sheet exceeds the row or column limit.")
            grid.reset_dimensions()
            for row in grid.iter_rows(max_col=MAX_COLUMNS + 1):
                if any(cell.data_type in ("f", "e") for cell in row):
                    raise IntakeError("Remove Excel formulas and error cells before uploading.")
                values = [cell.value for cell in row]
                while values and values[-1] is None:
                    values.pop()
                yield values
        finally:
            book.close()
    else:
        raise IntakeError("Choose CSV or XLSX.")


def normalize_cell(value, spec, timezone_name):
    if value is None or value == "":
        return None
    choices = spec.get("anyOf", [spec])
    types = {part.get("type") for part in choices}
    formats = {part.get("format") for part in choices}
    if isinstance(value, (datetime, date)):
        if "date" in formats and "date-time" not in formats:
            return value.date().isoformat() if isinstance(value, datetime) else value.isoformat()
        if "date-time" in formats and isinstance(value, datetime):
            if value.tzinfo is not None:
                return value.isoformat()
            try:
                zone = ZoneInfo(timezone_name)
            except (TypeError, ValueError, ZoneInfoNotFoundError):
                raise IntakeError("Use an IANA timezone for Excel timestamps.") from None
            first, second = (value.replace(tzinfo=zone, fold=fold) for fold in (0, 1))
            if first.utcoffset() != second.utcoffset() or first.astimezone(timezone.utc).astimezone(zone).replace(tzinfo=None) != value:
                raise IntakeError("Use ISO 8601 with an explicit offset for ambiguous or nonexistent Excel timestamps.")
            return first.isoformat()
        return value.isoformat()
    if not isinstance(value, str):
        return str(value) if spec.get("type") == "string" else value
    value = value.strip()
    if FORMULA.search(value):
        raise IntakeError("Formula-like input is not accepted.")
    if value.startswith(("{", "[")) and (spec.get("$ref") or {"object", "array"} & types):
        return json.loads(value)
    number = value.translate(DIGITS)
    if {"number", "integer"} & types and NUMBER.fullmatch(number):
        return json.loads(number)
    if "boolean" in types and value.lower() in ("true", "false"):
        return value.lower() == "true"
    if "string" in types and any("pattern" in part for part in choices):
        return number
    return value
