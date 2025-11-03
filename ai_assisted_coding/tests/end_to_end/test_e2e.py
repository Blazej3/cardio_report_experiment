from __future__ import annotations

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

import pytest
from main import render_html, write_pdf_from_html
from data_gen import generate_mock


def test_full_pipeline(tmp_path: Path):
    # Generate mock
    record = generate_mock(seed=42)

    # Render HTML
    html = render_html(record, template_dir=Path(__file__).resolve().parents[2])
    out_html = tmp_path / "report.html"
    out_html.write_text(html, encoding="utf-8")
    assert out_html.exists()
    assert out_html.stat().st_size > 0

    # PDF (skip if WeasyPrint is absent for any reason)
    weasyprint = pytest.importorskip("weasyprint")
    out_pdf = tmp_path / "report.pdf"
    write_pdf_from_html(html, out_pdf)
    assert out_pdf.exists()
    assert out_pdf.stat().st_size > 0
