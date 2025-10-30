"""tests for end to end functionality"""
import pytest
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))


from src.interpreter import interpret_vitals, classify_risk
from src.report_generator import build_report_model, generate_html_report, save_pdf

@pytest.fixture
def sample_patient():
    return {
  "patient_id": "Test123",
  "name": "End To End tester",
  "timestamp": "2025-10-29",
  "context": {
    "age_years": 40,
    "sex": "unknown",
    "notes": "Mock record"
  },
  "vitals": {
    "CCA": {
      "psv_cm_s": 210.0,
      "edv_cm_s": 110.0,
      "imt_mm": 1.2
    },
    "ICA": {
      "psv_cm_s": 130.0,
      "edv_cm_s": 45.0,
      "imt_mm": 1.1
    },
    "ECA": {
      "psv_cm_s": 160.0,
      "edv_cm_s": 45.0
    },
    "ica_cca_ratio": 4.2
  }
}

def test_end_to_end(sample_patient):
    findings = interpret_vitals(sample_patient)
    assert len(findings) > 0

    risk_level = classify_risk(findings)
    assert risk_level == "High"

    model = build_report_model(sample_patient, findings, risk_level)
    assert model["patient_name"] == "End To End tester"

    template_path = Path(__file__).parent.parent / "src" / "report_template.html"
    html = generate_html_report(model, template_path)

    output_path = Path(__file__).parent.parent / "tests" / "test_report.pdf"
    save_pdf(html, output_path, template_path.parent)

    assert output_path.exists()
    assert output_path.stat().st_size > 0

    output_path.unlink()
    assert not output_path.exists()
