"""Bounded document decoding in a child process with no application credentials."""

import io
import json
import os
import resource
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

from .intake_files import IntakeError, MAX_BYTES, check_package, rows_from_file
from .public_source import public_page


class TextNodes(HTMLParser):
    BLOCKS = {"article", "br", "div", "dt", "dd", "li", "p", "section", "tr",
              "h1", "h2", "h3", "h4", "h5", "h6"}
    EXCLUDED = {"script", "style", "template", "noscript"}

    def __init__(self):
        super().__init__()
        self.lines = []
        self.parts = []
        self.hidden = 0

    def finish_line(self):
        if self.parts:
            self.lines.append(" ".join(self.parts))
            self.parts.clear()

    def handle_starttag(self, tag, attrs):
        if tag in self.EXCLUDED:
            self.hidden += 1
        if self.hidden:
            return
        if tag in self.BLOCKS:
            self.finish_line()
        if tag == "meta":
            attrs = dict(attrs)
            if attrs.get("property") == "og:site_name" and attrs.get("content"):
                self.lines.append("company name: " + attrs["content"])

    def handle_endtag(self, tag):
        if tag in self.EXCLUDED and self.hidden:
            self.hidden -= 1
        if not self.hidden and tag in self.BLOCKS:
            self.finish_line()

    def handle_data(self, data):
        if not self.hidden and data.strip():
            self.parts.append(" ".join(data.split()))


def units(raw, extension):
    if extension in (".txt", ".html"):
        text = raw.decode("utf-8-sig")
        if extension == ".html":
            parser = TextNodes()
            parser.feed(text)
            parser.close()
            parser.finish_line()
            text = "\n".join(parser.lines)
        yield from ((f"line:{index}", line) for index, line in enumerate(text.splitlines(), 1))
    elif extension in (".xlsx", ".csv"):
        for index, row in enumerate(rows_from_file(raw, extension), 1):
            values = [str(cell) for cell in row if cell is not None]
            if len(values) == 2:
                yield f"row:{index}", ": ".join(values)
            else:
                yield f"row:{index}", " ".join(values)
    elif extension == ".pdf":
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(raw))
        if reader.is_encrypted or len(reader.pages) > 30:
            raise IntakeError("Use a text PDF with up to 30 pages.")
        for index, page in enumerate(reader.pages, 1):
            for offset, line in enumerate((page.extract_text() or "").splitlines(), 1):
                yield f"page:{index}/line:{offset}", line
    elif extension == ".docx":
        from docx import Document
        check_package(raw)
        for index, paragraph in enumerate(Document(io.BytesIO(raw)).paragraphs, 1):
            yield f"paragraph:{index}", paragraph.text
    elif extension == ".pptx":
        from pptx import Presentation
        check_package(raw)
        for index, slide in enumerate(Presentation(io.BytesIO(raw)).slides, 1):
            for offset, shape in enumerate(slide.shapes, 1):
                if shape.has_text_frame:
                    for line in shape.text.splitlines():
                        yield f"slide:{index}/shape:{offset}", line
    else:
        raise IntakeError("Choose PDF, DOCX, XLSX, PPTX, text or CSV.")


def process(mode, payload):
    allowed = {"PATH", "LANG", "LC_ALL", "TZ", "SSL_CERT_FILE", "SSL_CERT_DIR"}
    environ = {key: value for key, value in os.environ.items() if key in allowed}
    environ.update(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", PYTHONUTF8="1")
    try:
        child = subprocess.run(
            [sys.executable, "-m", "core.intake_sandbox", mode],
            input=payload, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            cwd=Path(__file__).resolve().parents[1], env=environ, timeout=14, check=False,
        )
        result = json.loads(child.stdout)
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        raise IntakeError("The source could not be read within the intake limits.") from exc
    if child.returncode != 0 or "error" in result:
        raise IntakeError(result.get("error", "The source could not be read."))
    return result


def main(mode):
    import base64
    resource.setrlimit(resource.RLIMIT_CPU, (8, 8))
    resource.setrlimit(resource.RLIMIT_AS, (768 * 1024 ** 2, 768 * 1024 ** 2))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_FSIZE, (8_000_000, 8_000_000))
    try:
        if mode == "fetch":
            raw, mime = public_page(sys.stdin.buffer.read(201).decode("ascii"))
            result = {"raw": base64.b64encode(raw).decode("ascii"), "mime": mime}
        else:
            raw = sys.stdin.buffer.read(MAX_BYTES + 1)
            if len(raw) > MAX_BYTES:
                raise IntakeError("The selected document exceeds the size limit.")
            lines, size = [], 0
            for anchor, text in units(raw, mode):
                size += len(text)
                if len(lines) >= 5000 or size > 400_000:
                    raise IntakeError("The source contains too much text.")
                lines.append((anchor, text))
            result = {"lines": lines}
        print(json.dumps(result, ensure_ascii=False))
    except Exception as exc:
        print(json.dumps({"error": str(exc) if isinstance(exc, IntakeError) else
                          "Use a readable, unencrypted document with selectable text."}))
        raise SystemExit(1) from None


if __name__ == "__main__":
    main(sys.argv[1])
