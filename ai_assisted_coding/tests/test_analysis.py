from __future__ import annotations

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from analysis import analyze


def test_analyze_basic_stats():
    data = {
        "vitals": {
            "CCA": {"psv_cm_s": 100.0, "edv_cm_s": 20.0, "imt_mm": 0.5},
            "ICA": {"psv_cm_s": 150.0, "edv_cm_s": 30.0, "imt_mm": 0.7},
            "ECA": {"psv_cm_s": 60.0,  "edv_cm_s": 25.0},
            "ica_cca_ratio": 1.23,
        }
    }
    a = analyze(data)
    assert a["psv"] is not None
    assert a["psv"]["min"] == 60.0
    assert a["psv"]["max"] == 150.0

    assert abs(a["psv"]["mean"] - (100 + 150 + 60) / 3) < 1e-9

    assert a["edv"]["min"] == 20.0
    assert a["edv"]["max"] == 30.0
    assert a["imt"]["min"] == 0.5
    assert a["imt"]["max"] == 0.7

    assert a["highest_psv_vessel"] == "ICA"
    assert a["ica_cca_ratio"] == 1.23
    assert any("Highest PSV" in note for note in a["notes"])
