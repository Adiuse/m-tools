"""Render the same frozen report data to the four executive formats."""

import html
import io
import json
import math
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


def include(snapshot, section):
    return "include_sections" not in snapshot or section in snapshot["include_sections"]


def rows(snapshot, *, compact=False):
    model = snapshot["model"]
    fa = model["locale"] == "fa"
    yield ("عنوان" if fa else "Title", model["title"])
    yield ("وضعیت" if fa else "Status", model["status"])
    if include(snapshot, "summary"):
        yield ("خلاصه" if fa else "Summary", model["executive_summary"])
    yield ("پوشش" if fa else "Coverage", model["coverage"]["status"])
    yield ("واحد / ارز" if fa else "Unit / currency", model["currency"])
    yield ("نسخه و منبع" if fa else "Source and version", snapshot["source"])
    yield ("شناسهٔ نسخه" if fa else "Snapshot checksum", model["checksum"])
    for card in model["kpi_cards"] if include(snapshot, "kpis") else []:
        yield (card["metric_key"] + " · " + card["unit"], Decimal(card["value"]) if card["value"] is not None else None)
    for text in model["methodology"] if include(snapshot, "methodology") else []:
        yield ("روش" if fa else "Method", text)
    for assumption in model["assumptions"] if include(snapshot, "methodology") else []:
        yield (assumption["label"], assumption["value"])
    for text in model["limitations"]:
        yield ("محدودیت" if fa else "Limitation", text)
    tables = snapshot.get("tables")
    if tables is None:
        tables = [{"title": model["title"], "columns": snapshot["columns"], "rows": snapshot["rows"]}]
    for table in tables if include(snapshot, "tables") else []:
        yield (table["title"],)
        columns = table["columns"]
        if compact and len(columns) > 6:
            for index, row in enumerate(table["rows"], 1):
                yield ("ردیف" if fa else "Row", index)
                yield from ((key, row.get(key)) for key in columns)
        else:
            yield tuple(columns)
            yield from (tuple(row.get(key) for key in columns) for row in table["rows"])
    for chart in snapshot.get("charts", []) if include(snapshot, "charts") else []:
        yield (chart["title"], "دادهٔ نمودار" if fa else "Chart data")
        yield tuple(chart["columns"])
        yield from map(tuple, chart["rows"])


def native_charts(snapshot):
    if not include(snapshot, "charts"):
        return []
    return [chart for chart in snapshot.get("charts", []) if chart["numeric"] and chart["type"] in ("line", "bar")]


def docx(snapshot, output):
    from docx import Document
    from docx.oxml import OxmlElement
    from docx.enum.table import WD_TABLE_DIRECTION
    book = Document()
    items = list(rows(snapshot, compact=True))
    table = book.add_table(rows=0, cols=max(2, max(map(len, items))))
    table.style = "Table Grid"
    if snapshot["model"]["locale"] == "fa":
        table.table_direction = WD_TABLE_DIRECTION.RTL
    for row in items:
        cells = table.add_row().cells
        for cell, value in zip(cells, row):
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
    items = list(rows(snapshot))
    worksheet.set_column(0, max(1, max(map(len, items)) - 1), 34)
    worksheet.freeze_panes(1, 0)
    for index, row in enumerate(items):
        for column, value in enumerate(row):
            if value is not None:
                worksheet.write(index, column, display(value) if isinstance(value, (dict, list)) else value)
    for index, spec in enumerate(native_charts(snapshot), 1):
        data = book.add_worksheet(f"Chart {index}")
        if snapshot["model"]["locale"] == "fa":
            data.right_to_left()
        data.write_row(0, 0, spec["columns"])
        for row_index, row in enumerate(spec["rows"], 1):
            data.write_row(row_index, 0, [display(row[0]), *row[1:]])
        chart = book.add_chart({"type": "line" if spec["type"] == "line" else "column"})
        for column in range(1, len(spec["columns"])):
            chart.add_series({"name": [data.name, 0, column],
                              "categories": [data.name, 1, 0, len(spec["rows"]), 0],
                              "values": [data.name, 1, column, len(spec["rows"]), column]})
        chart.set_title({"name": spec["title"]})
        data.insert_chart(1, len(spec["columns"]) + 1, chart)
    book.close()


def pptx(snapshot, output):
    from pptx import Presentation
    from pptx.chart.data import CategoryChartData
    from pptx.enum.chart import XL_CHART_TYPE
    from pptx.enum.text import PP_ALIGN
    from pptx.util import Inches, Pt
    items = list(rows(snapshot, compact=True))
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
    for spec in native_charts(snapshot):
        slide = deck.slides.add_slide(deck.slide_layouts[6])
        data = CategoryChartData()
        data.categories = [display(row[0]) for row in spec["rows"]]
        for column, title in enumerate(spec["columns"][1:], 1):
            data.add_series(title, [row[column] for row in spec["rows"]])
        kind = XL_CHART_TYPE.LINE if spec["type"] == "line" else XL_CHART_TYPE.COLUMN_CLUSTERED
        chart = slide.shapes.add_chart(kind, Inches(.8), Inches(.65), Inches(11.7), Inches(6), data).chart
        chart.has_title = True
        chart.chart_title.text_frame.text = spec["title"]
    deck.save(output)


def svg_chart(spec):
    """Render line/column charts from the exact frozen series, with gaps for nulls."""
    points = spec["rows"]
    numeric = [float(value) for row in points for value in row[1:] if value is not None]
    if not numeric or not all(map(math.isfinite, numeric)):
        return ""
    low, high = min(0, min(numeric)), max(0, max(numeric))
    span = high - low or 1
    if not math.isfinite(span):
        return ""
    width, height = 490, 146
    left, top = 53, 12
    step = width / len(points)
    bottom = top + height
    baseline = top + high / span * height
    colors = ("#08684f", "#255c93", "#964c18", "#63498a")
    svg = [f'<path d="M{left} {top}v{height}M{left} {baseline:.2f}h{width}" stroke="#526461" fill="none"/>']
    for label, y in ((high, top + 10), (low, bottom)):
        svg.append(f'<text x="47" y="{y}" text-anchor="end">{label:.4g}</text>')
    count = len(spec["columns"]) - 1
    for column, name in enumerate(spec["columns"][1:], 1):
        color = colors[(column - 1) % len(colors)]
        segments, current = [], []
        for index, point in enumerate(points):
            value = point[column]
            if value is None:
                if current:
                    segments.append(current)
                    current = []
                continue
            x = left + (index + .5) * step
            y = top + (high - float(value)) / span * height
            if spec["type"] == "bar":
                bar = step * .66 / count
                offset = (column - 1) * bar - step * .33
                svg.append(f'<rect x="{x+offset:.2f}" y="{min(y, baseline):.2f}" width="{bar:.2f}" '
                           f'height="{abs(y-baseline):.2f}" fill="{color}"/>')
            else:
                current.append(f"{x:.2f},{y:.2f}")
                svg.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2.8" fill="{color}"/>')
        for segment in [*segments, current]:
            if segment:
                svg.append(f'<polyline points="{" ".join(segment)}" stroke="{color}" stroke-width="2" fill="none"/>')
    for index in sorted({0, len(points) // 2, len(points) - 1}):
        label = html.escape(display(points[index][0])[:22])
        svg.append(f'<text x="{left+(index+.5)*step:.2f}" y="{bottom+18}" text-anchor="middle">{label}</text>')
    legend = " · ".join(
        f'<span style="color:{colors[index % len(colors)]}">{html.escape(name)}</span>'
        for index, name in enumerate(spec["columns"][1:])
    )
    return ('<figure><figcaption>' + html.escape(spec["title"]) + '</figcaption>'
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 185" style="font:10px sans-serif">'
            + "".join(svg) + '</svg><p>' + legend + '</p></figure>')


def pdf(snapshot, output):
    binary = os.environ.get("MTOOLS_PDF_CHROMIUM")
    if not binary:
        raise ValueError("The PDF renderer is not configured.")
    rtl = snapshot["model"]["locale"] == "fa"
    items = list(rows(snapshot, compact=True))
    columns = max(2, max(map(len, items)))
    table_rows = []
    for row in items:
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
            'td{border:1px solid #ddd;padding:6px;overflow-wrap:anywhere}figure{break-inside:avoid;margin:12px 0}'
            'svg{width:100%;max-height:56mm}</style><table>' + table + '</table>'
            + "".join(svg_chart(chart) for chart in native_charts(snapshot)),
            encoding="utf-8",
        )
        file = base / "report.pdf"
        args = [binary, "--headless", "--disable-background-networking", "--disable-extensions",
                "--no-pdf-header-footer", f"--user-data-dir={base / 'browser'}", f"--print-to-pdf={file}"]
        subprocess.run([*args, page.as_uri()], check=True, timeout=45, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        output.write(file.read_bytes())


def render(snapshot, format_name):
    output = io.BytesIO()
    {"pdf": pdf, "docx": docx, "xlsx": xlsx, "pptx": pptx}[format_name](snapshot, output)
    result = output.getvalue()
    if len(result) > 12_000_000:
        raise ValueError("The generated report exceeds the output limit.")
    return result
