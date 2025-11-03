from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML

from analysis import analyze
from data_gen import generate_mock


def _title_case_name(name: str) -> str:
    """Title-case a patient name conservatively."""
    return " ".join(part.capitalize() for part in name.split())


def _vitals_rows(vitals: Dict[str, Any]) -> List[Dict[str, Optional[float]]]:
    rows: List[Dict[str, Optional[float]]] = []
    for vessel, payload in vitals.items():
        if vessel == "ica_cca_ratio":
            continue
        if not isinstance(payload, dict):
            continue
        rows.append({
            "vessel": vessel,
            "psv": payload.get("psv_cm_s"),
            "edv": payload.get("edv_cm_s"),
            "imt": payload.get("imt_mm"),
        })

    pref = {"CCA": 0, "ICA": 1, "ECA": 2}
    rows.sort(key=lambda r: pref.get(str(r["vessel"]), 99))
    return rows


def render_html(data: Dict[str, Any], template_dir: Path) -> str:
    """
    Render HTML string using Jinja2 template and analysis output.
    """
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(["html"])
    )
    tmpl = env.get_template("report_template.html")

    a = analyze(data)
    vitals = data.get("vitals", {})

    payload = {
        "patient_name": _title_case_name(data.get("name", "unknown")),
        "patient_id": data.get("patient_id", "n/a"),
        "timestamp": data.get("timestamp", "n/a"),
        "context": data.get("context", {}),
        "vitals_rows": _vitals_rows(vitals),
        "stats": a,
        "highest_psv_vessel": a.get("highest_psv_vessel"),
        "ica_cca_ratio": a.get("ica_cca_ratio"),
        "notes": a.get("notes", []),
    }
    return tmpl.render(**payload)


def write_pdf_from_html(html: str, out_pdf: Path) -> None:
    """
    Generate a PDF from an HTML string using WeasyPrint.
    """
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html, base_url=str(out_pdf.parent)).write_pdf(str(out_pdf))


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: Path, obj: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a non-medical, descriptive cardio report (HTML + PDF)."
    )
    parser.add_argument("--in", dest="in_path", type=str, help="Path to input JSON.")
    parser.add_argument("--generate-mock", action="store_true", help="Generate mock JSON instead of reading input.")
    parser.add_argument("--out", dest="out_dir", type=str, default="out", help="Output directory (default: out)")
    parser.add_argument("--seed", dest="seed", type=int, default=None, help="Optional RNG seed for mock generation.")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    template_dir = Path(__file__).parent

    if args.generate_mock:
        data = generate_mock(seed=args.seed)
    else:
        if not args.in_path:
            raise SystemExit("Please provide --in <path> or use --generate-mock.")
        data = _load_json(Path(args.in_path))

    _write_json(out_dir / "normalized_input.json", data)

    html = render_html(data, template_dir=template_dir)
    out_html = out_dir / "report.html"
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(html, encoding="utf-8")

    out_pdf = out_dir / "report.pdf"
    write_pdf_from_html(html, out_pdf=out_pdf)

    print(f"Wrote: {out_html}")
    print(f"Wrote: {out_pdf}")


if __name__ == "__main__":
    main()
