"""tests fr interpreter module"""
import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.interpreter import interpret_vitals, classify_risk

@pytest.fixture
def normal_vitals():
    return {
        "CCA": {"psv_cm_s": 100, "edv_cm_s": 30, "imt_mm": 0.8},
        "ICA": {"psv_cm_s": 120, "edv_cm_s": 35, "imt_mm": 0.9},
        "ECA": {"psv_cm_s": 130, "edv_cm_s": 25},
        "ica_cca_ratio": 1.2
    }
@pytest.fixture
def severe_vitals():
    return {
        "CCA": {"psv_cm_s": 130, "edv_cm_s": 45, "imt_mm": 1.2},
        "ICA": {"psv_cm_s": 210, "edv_cm_s": 110, "imt_mm": 1.3},
        "ECA": {"psv_cm_s": 160, "edv_cm_s": 50},
        "ica_cca_ratio": 4.5
    }

def test_interpret_vitals_normal(normal_vitals):
    findings = interpret_vitals({"vitals":normal_vitals})
    assert findings == [], f"Expected no finding, but got: {findings}"

def test_interpret_vitals_severe(severe_vitals):
    findings = interpret_vitals({"vitals":severe_vitals})
    expected_findings = [
        "Severe ICA PSV, stenosis (>70%)",
        "Severe ICA EDV (>100 cm/s)",
        "Elevated ICA IMT (>1.0 mm)",
        "Elevated CCA PSV (>125 cm/s)",
        "Elevated CCA EDV (>40 cm/s)",
        "Elevated CCA IMT (>1.0 mm)",
        "Elevated ECA PSV (>150 cm/s)",
        "Elevated ECA EDV (>40 cm/s)",
        "Severe ICA/CCA suggests stenosis (>70%)."
    ]
    for finding in findings:
        assert finding in expected_findings, f"Unexpected finding: {finding}"

def test_classify_risk_normal():
    findings = ["No significant findings, or Normal findings"]
    risk = classify_risk(findings)
    assert risk == "Normal", f"Expected Normal risk level, but got: {risk}"

def test_classify_risk_moderate():
    findings = ["Moderate ICA PSV, stenosis (50-69%)", "Elevated CCA PSV (>125 cm/s), Mildly elevated ICA/CCA ratio."]
    risk = classify_risk(findings)
    assert risk == "Moderate", f"Expected Moderate risk level, but got: {risk}"

def test_classify_risk_high():
    findings = ["Severe ICA PSV, stenosis (>70%)"]
    risk = classify_risk(findings)
    assert risk == "High", f"Expected High risk level, but got: {risk}"
