from __future__ import annotations
from pathlib import Path
from typing import Any
from weasyprint import HTML

from jinja2 import Environment, FileSystemLoader, select_autoescape

def _fmt(v : Any):
    return f"{v:.2f}".rstrip('0').rstrip('.')

def _unit_for(metric: str):
    if "psv" in metric or "edv" in metric:
        return "cm/s" 
    if "imt" in metric:
        return "mm"
    return ""

def _section_from_vitals(vitals: dict):
    
    sections = ["ICA", "CCA", "ECA"]
    out_sections = []
    for section in sections:
        val = vitals.get(section)
        rows = []
        for k, v in val.items():
            rows.append({"metric": k, "value": _fmt(v), "unit": _unit_for(k)})
        out_sections.append({"section": section, "rows": rows})

    derived = [ {"metric": "ICA/CCA Ratio","value": _fmt(vitals["ica_cca_ratio"]),"unit": ""}]
   
    return out_sections, derived

def build_report_model(patient:dict, findings:list[str], risk_level:str):
    vitals = patient.get("vitals")
    sections, derived = _section_from_vitals(vitals)
    return {
        "patient_id": patient.get("patient_id"),
        "patient_name": patient.get("name"),
        "exam_date": patient.get("timestamp"),
        "vital_sections": sections,
        "derived_metrics": derived,
        "findings": findings,
        "risk_level": risk_level
    }
def generate_html_report(model:dict, template_path:Path):
    env = Environment(
        loader=FileSystemLoader(template_path.parent),
        autoescape=select_autoescape(['html', 'xml']),
        trim_blocks=True,
        lstrip_blocks=True
    )
    return env.get_template(template_path.name).render(model)

def save_pdf(html:str, output:Path, template_dir: Path):
    output.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html, base_url=str(template_dir)).write_pdf(str(output))
