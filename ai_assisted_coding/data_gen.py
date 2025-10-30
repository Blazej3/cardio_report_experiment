from __future__ import annotations

import random
from datetime import date
from typing import Any, Dict, Optional


def _rand_range(rng: random.Random, low: float, high: float, nd: int = 1) -> float:
    """Inclusive-uniform in [low, high] rounded to nd decimals."""
    return round(rng.uniform(low, high), nd)


def generate_mock(seed: Optional[int] = None) -> Dict[str, Any]:
    """
    Generate a plausible mock JSON compatible with the expected schema.
    Ranges are intentionally broad and **non-medical**.

    Returns:
        Dict with keys: patient_id, name, timestamp, context, vitals.
    """
    rng = random.Random(seed)

    # Plausible broad ranges (not medical guidance)
    # PSV cm/s: CCA 50–200, ICA 70–250, ECA 40–180
    # EDV cm/s: CCA 10–40, ICA 15–60,  ECA 5–35
    # IMT mm:   CCA/ICA 0.4–1.2
    cca = {
        "psv_cm_s": _rand_range(rng, 50, 200, 1),
        "edv_cm_s": _rand_range(rng, 10, 40, 1),
        "imt_mm": _rand_range(rng, 0.4, 1.2, 2),
    }
    ica = {
        "psv_cm_s": _rand_range(rng, 70, 250, 1),
        "edv_cm_s": _rand_range(rng, 15, 60, 1),
        "imt_mm": _rand_range(rng, 0.4, 1.2, 2),
    }
    eca = {
        "psv_cm_s": _rand_range(rng, 40, 180, 1),
        "edv_cm_s": _rand_range(rng, 5, 35, 1),
    }
    ratio = round(ica["psv_cm_s"] / cca["psv_cm_s"], 2) if cca["psv_cm_s"] else None

    record: Dict[str, Any] = {
        "patient_id": str(rng.randint(10000, 99999)),
        "name": rng.choice(["alex martin", "casey lee", "jordan taylor", "morgan kim"]),
        "timestamp": str(date.today()),
        "context": {
            "age_years": rng.randint(20, 85),
            "sex": rng.choice(["unknown", "female", "male"]),
            "notes": "Mock record",
        },
        "vitals": {
            "CCA": cca,
            "ICA": ica,
            "ECA": eca,
            "ica_cca_ratio": ratio,
        },
    }
    return record
