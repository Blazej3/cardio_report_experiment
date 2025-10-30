from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Any, Dict, List, Optional, Tuple


@dataclass(frozen=True)
class StatTriple:
    """Simple container for min/max/mean of numeric series."""
    min: float
    max: float
    mean: float


def _collect_metric(vitals: Dict[str, Any], metric_key: str) -> List[Tuple[str, float]]:
    """
    Collect (vessel, value) for a given metric across vessel dicts in vitals.

    Args:
        vitals: The 'vitals' dict from input JSON.
        metric_key: One of 'psv_cm_s', 'edv_cm_s', 'imt_mm'.

    Returns:
        List of (vessel_name, value) pairs where the metric exists and is numeric.
    """
    results: List[Tuple[str, float]] = []
    for vessel, payload in vitals.items():
        if vessel == "ica_cca_ratio":
            continue
        if isinstance(payload, dict) and metric_key in payload:
            val = payload[metric_key]
            if isinstance(val, (int, float)):
                results.append((vessel, float(val)))
    return results


def _stats(values: List[float]) -> Optional[StatTriple]:
    """Compute min/max/mean if values exist, otherwise None."""
    if not values:
        return None
    return StatTriple(min=min(values), max=max(values), mean=mean(values))


def analyze(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Produce a purely descriptive analysis of PSV/EDV/IMT across available vessels.

    Returns:
        Dict containing:
        - 'psv': StatTriple as dict or None
        - 'edv': StatTriple as dict or None
        - 'imt': StatTriple as dict or None
        - 'highest_psv_vessel': name or None
        - 'ica_cca_ratio': float or None
        - 'notes': short descriptive bullet points
    """
    vitals = data.get("vitals", {})
    psv_pairs = _collect_metric(vitals, "psv_cm_s")
    edv_pairs = _collect_metric(vitals, "edv_cm_s")
    imt_pairs = _collect_metric(vitals, "imt_mm")

    psv_values = [v for _, v in psv_pairs]
    edv_values = [v for _, v in edv_pairs]
    imt_values = [v for _, v in imt_pairs]

    psv_stats = _stats(psv_values)
    edv_stats = _stats(edv_values)
    imt_stats = _stats(imt_values)

    highest_psv_vessel = None
    if psv_pairs:
        highest_psv_vessel = max(psv_pairs, key=lambda x: x[1])[0]

    ratio = vitals.get("ica_cca_ratio")
    ratio_val = float(ratio) if isinstance(ratio, (int, float)) else None

    def triple_to_dict(t: Optional[StatTriple]) -> Optional[Dict[str, float]]:
        return None if t is None else {"min": t.min, "max": t.max, "mean": t.mean}

    notes: List[str] = []
    if highest_psv_vessel:
        notes.append(f"Highest PSV observed in: {highest_psv_vessel}.")
    if ratio_val is not None:
        notes.append(f"ICA/CCA PSV ratio (echoed): {ratio_val:.2f}.")
    if imt_stats is not None:
        notes.append("IMT values summarized descriptively (no thresholds applied).")

    return {
        "psv": triple_to_dict(psv_stats),
        "edv": triple_to_dict(edv_stats),
        "imt": triple_to_dict(imt_stats),
        "highest_psv_vessel": highest_psv_vessel,
        "ica_cca_ratio": ratio_val,
        "notes": notes,
    }
