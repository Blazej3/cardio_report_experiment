import pytest
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from src.report_generator import (_fmt, _unit_for, _section_from_vitals, build_report_model, generate_html_report)

@pytest.fixture
def sample_patient():
    return {
  "patient_id": "Test123",
  "name": "John Tester",
  "timestamp": "2025-10-29",
  "context": {
    "age_years": 40,
    "sex": "unknown",
    "notes": "Mock record"
  },
  "vitals": {
    "CCA": {
      "psv_cm_s": 149.3,
      "edv_cm_s": 20.7,
      "imt_mm": 0.67
    },
    "ICA": {
      "psv_cm_s": 195.5,
      "edv_cm_s": 31.7,
      "imt_mm": 0.89
    },
    "ECA": {
      "psv_cm_s": 58.9,
      "edv_cm_s": 23.0
    },
    "ica_cca_ratio": 1.31
  }
}

@pytest.fixture
def mock_findings():
    return ["Increased PSV in ICA","Elevated IMT in CCA"]

def test_fmt():
    assert _fmt(123.4567) == "123.46"
    assert _fmt(100.0) == "100"
    assert _fmt(0.0) == "0"
    assert _fmt(3.1) == "3.1"

def test_unit_for():
    assert _unit_for("psv_cm_s") == "cm/s"
    assert _unit_for("edv_cm_s") == "cm/s"
    assert _unit_for("imt_mm") == "mm"
    assert _unit_for("other_metric") == ""

def test_section_from_vitals(sample_patient):
    sections, derived = _section_from_vitals(sample_patient["vitals"])
    assert len(sections) == 3
    for section in sections:
        assert section["section"] in ["ICA", "CCA", "ECA"]

    assert len(derived) == 1
    assert derived[0]["metric"] == "ICA/CCA Ratio"
    assert derived[0]["value"] == "1.31"

def test_build_report_model(sample_patient, mock_findings):
    model = build_report_model(sample_patient, mock_findings, "Moderate")
    assert model["patient_id"] == "Test123"
    assert model["patient_name"] == "John Tester"
    assert model["exam_date"] == "2025-10-29"
    assert len(model["vital_sections"]) == 3
    assert len(model["derived_metrics"]) == 1
    assert model["findings"] == mock_findings
    assert model["risk_level"] == "Moderate"

def test_generate_html_report(sample_patient, mock_findings):
    template_content = """
    <html>
    <head><title>Report for {{ patient_name }}</title></head>
    <body>
        <h1>Patient ID: {{ patient_id }}</h1>
        <h2>Exam Date: {{ exam_date }}</h2>
        <h3>Findings:</h3>
        <ul>
        {% for finding in findings %}
            <li>{{ finding }}</li>
        {% endfor %}
        </ul>
    </body>
    </html>
    """
    template_path = Path(__file__).parent.parent / "tests" / "report_template.html"
    template_path.write_text(template_content)

    model = build_report_model(sample_patient, mock_findings, "Moderate")
    html = generate_html_report(model, template_path)

    assert "<title>Report for John Tester</title>" in html
    assert "<h1>Patient ID: Test123</h1>" in html
    assert "<h2>Exam Date: 2025-10-29</h2>" in html

    template_path.unlink()
    assert not template_path.exists()

