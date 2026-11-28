"""Render the same frozen report data to the four executive formats."""

import html
import io
import json
import os
import subprocess
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory

FORMAT_MIME = {
    "pdf": "application/pdf",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
}


def display(value):
    if value is None:
        return "—"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def rows(snapshot):
    model = snapshot["model"]
    fa = model["locale"] == "fa"
    yield ("عنوان" if fa else "Title", model["title"])
    yield ("وضعیت" if fa else "Status", model["status"])
    yield ("خلاصه" if fa else "Summary", model["executive_summary"])
    yield ("واحد / ارز" if fa else "Unit / currency", model["currency"])
    yield ("نسخه و منبع" if fa else "Source and version", snapshot["source"])
    yield ("شناسهٔ نسخه" if fa else "Snapshot checksum", model["checksum"])
    for card in model["kpi_cards"]:
        yield (card["metric_key"] + " · " + card["unit"], Decimal(card["value"]) if card["value"] is not None else None)
    for text in model["limitations"]:
        yield ("محدودیت" if fa else "Limitation", text)
    if snapshot["rows"]:
        yield tuple(snapshot["columns"])
        yield from (tuple(row.get(key) for key in snapshot["columns"]) for row in snapshot["rows"])


def docx(snapshot, output):
    from docx import Document
    from docx.oxml import OxmlElement
    from docx.enum.table import WD_TABLE_DIRECTION
    book = Document()
    table = book.add_table(rows=0, cols=max(2, len(snapshot["columns"])))
    table.style = "Table Grid"
    if snapshot["model"]["locale"] == "fa":
        table.table_direction = WD_TABLE_DIRECTION.RTL
    for row in rows(snapshot):
        for cell, value in zip(table.add_row().cells, row):
            paragraph = cell.paragraphs[0]
            if snapshot["model"]["locale"] == "fa":
                paragraph._p.get_or_add_pPr().append(OxmlElement("w:bidi"))
            run = paragraph.add_run(display(value))
            run.font.rtl = snapshot["model"]["locale"] == "fa"
    book.save(output)


def xlsx(snapshot, output):
    import xlsxwriter
    book = xlsxwriter.Workbook(output, {"in_memory": True, "strings_to_urls": False, "strings_to_formulas": False})
    worksheet = book.add_worksheet("Report")
    if snapshot["model"]["locale"] == "fa":
        worksheet.right_to_left()
    worksheet.set_column(0, max(1, len(snapshot["columns"]) - 1), 34)
    worksheet.freeze_panes(1, 0)
    for index, row in enumerate(rows(snapshot)):
        for column, value in enumerate(row):
            if value is not None:
                worksheet.write(index, column, display(value) if isinstance(value, (dict, list)) else value)
    book.close()


def pptx(snapshot, output):
    from pptx import Presentation
    from pptx.enum.text import PP_ALIGN
    from pptx.util import Inches, Pt
    items = list(rows(snapshot))
    deck = Presentation()
    deck.slide_width, deck.slide_height = Inches(13.333), Inches(7.5)
    rtl = snapshot["model"]["locale"] == "fa"
    for offset in range(0, len(items), 8):
        slide = deck.slides.add_slide(deck.slide_layouts[6])
        heading = slide.shapes.add_textbox(Inches(.65), Inches(.3), Inches(12), Inches(.65))
        heading.text = snapshot["model"]["title"]
        heading.text_frame.paragraphs[0].font.size = Pt(24)
        if rtl:
            heading.text_frame.paragraphs[0]._p.get_or_add_pPr().set("rtl", "1")
            heading.text_frame.paragraphs[0].alignment = PP_ALIGN.RIGHT
        batch = items[offset:offset + 8]
        columns = max(2, max(map(len, batch)))
        table = slide.shapes.add_table(len(batch), columns, Inches(.65), Inches(1.2), Inches(12), Inches(5.5)).table
        for index, row in enumerate(batch):
            for column, value in enumerate(row):
                paragraph = table.cell(index, columns - column - 1 if rtl else column).text_frame.paragraphs[0]
                if rtl:
                    paragraph._p.get_or_add_pPr().set("rtl", "1")
                    paragraph.alignment = PP_ALIGN.RIGHT
                paragraph.text = display(value)
                paragraph.font.size = Pt(12)
    deck.save(output)


def pdf(snapshot, output):
    binary = os.environ.get("MTOOLS_PDF_CHROMIUM")
    if not binary:
        raise ValueError("The PDF renderer is not configured.")
    rtl = snapshot["model"]["locale"] == "fa"
    columns = max(2, len(snapshot["columns"]))
    table_rows = []
    for row in rows(snapshot):
        cells = []
        for index, value in enumerate(row):
            span = columns - len(row) + 1 if index == len(row) - 1 else 1
            cells.append(f'<td colspan="{span}">' + html.escape(display(value)) + "</td>")
        table_rows.append("<tr>" + "".join(cells) + "</tr>")
    table = "".join(table_rows)
    with TemporaryDirectory(prefix="mtools-report-") as directory:
        base = Path(directory)
        page = base / "report.html"
        page.write_text(
            '<!doctype html><html dir="' + ("rtl" if rtl else "ltr") + '"><meta charset="utf-8">'
            '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'">'
            '<style>@page{size:A4;margin:16mm;@bottom-center{content:counter(page)}}body{font:12pt sans-serif;color:#183b37}'
            'table{border-collapse:collapse;width:100%;table-layout:fixed}tr{break-inside:avoid}'
            'td{border:1px solid #ddd;padding:6px;overflow-wrap:anywhere}</style><table>' + table + '</table>',
            encoding="utf-8",
        )
        file = base / "report.pdf"
        args = [binary, "--headless", "--disable-background-networking", "--disable-extensions",
                "--no-pdf-header-footer", f"--user-data-dir={base / 'browser'}", f"--print-to-pdf={file}"]
        if os.environ.get("MTOOLS_DEBUG") == "1" and os.environ.get("MTOOLS_PDF_DEV_NO_SANDBOX") == "1":
            args.append("--no-sandbox")
        subprocess.run([*args, page.as_uri()], check=True, timeout=45, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        output.write(file.read_bytes())


def render(snapshot, format_name):
    output = io.BytesIO()
    {"pdf": pdf, "docx": docx, "xlsx": xlsx, "pptx": pptx}[format_name](snapshot, output)
    result = output.getvalue()
    if len(result) > 12_000_000:
        raise ValueError("The generated report exceeds the output limit.")
    return result
