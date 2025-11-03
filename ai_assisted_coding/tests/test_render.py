from __future__ import annotations

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from main import render_html


def test_template_renders(tmp_path: Path):
    data = {
        "patient_id": "99999",
        "name": "jane doe",
        "timestamp": "2025-10-29",
        "context": {"age_years": 33, "sex": "female", "notes": "Unit test"},
        "vitals": {
            "CCA": {"psv_cm_s": 120.0, "edv_cm_s": 22.0, "imt_mm": 0.6},
            "ICA": {"psv_cm_s": 180.0, "edv_cm_s": 28.0, "imt_mm": 0.8},
            "ECA": {"psv_cm_s": 55.0,  "edv_cm_s": 21.0},
            "ica_cca_ratio": 1.50
        }
    }
    template_dir = Path(__file__).resolve().parents[1]
    html = render_html(data, template_dir=template_dir)
    assert "<!doctype html>" in html
    assert "Cardio Report (Descriptive Only)" in html
    assert "Highest PSV" in html
    assert "ICA/CCA PSV ratio" in html
