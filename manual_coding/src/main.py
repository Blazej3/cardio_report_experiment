
import json
from pathlib import Path
from report_generator import build_report_model, generate_html_report, save_pdf
from interpreter import interpret_vitals, classify_risk


def load_patient_data(file_path: Path):
    """Loads patient data from Json"""
    with open(file_path, 'r') as f:
        return json.load(f)

def main():
    project_root = Path(__file__).parent.parent
    
    patient_data = load_patient_data(project_root / "data" / "mock_patient.json")
    
    findings = interpret_vitals(patient_data)
    risk_level = classify_risk(findings)

    report_model = build_report_model(patient_data, findings, risk_level)

    template_path = project_root / "src" / "report_template.html"
    html_report = generate_html_report(report_model, template_path)

    output_path = project_root / "output" / "patient_report.pdf"
    save_pdf(html_report, output_path, template_path.parent)

if __name__ == "__main__":
    main()