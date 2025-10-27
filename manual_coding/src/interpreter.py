def interpret_vitals(patient:dict):
    
    findings = []
    vitals = patient.get("vitals", {})

    cca = vitals.get("CCA", {})
    ica = vitals.get("ICA", {})
    eca = vitals.get("ECA", {})
    ratio = vitals.get("ica_cca_ratio", {})

    ica_psv = ica.get("psv_cm_s")
    cca_psv = cca.get("psv_cm_s")

    if ica_psv:
        if ica_psv > 200:
            findings.append("Severe ICA stenosis (>70%).")
        elif ica_psv > 125:
            findings.append("Moderate ICA stenosis (50-69%).")
        else:
            findings.append("Mild or no ICA stenosis (<50%).")
    
    if ratio:
        if ratio > 2.0:
            findings.append("Elevated ICA/CCA suggest stenosis (>50%).")
        elif ratio > 1.5:
            findings.append("Mildly elevated ICA/CCA ratio.")
        else:
            findings.append("Normal ICA/CCA ratio.")

    imt = cca.get("imt_mm")
    if imt:
        if imt >= 1.1:
            findings.append("Increased CCA IMT (>1.0 mm).")
        else:
            findings.append("Normal CCA IMT (<1.0mm).")
    
    eca_psv = eca.get("psv_cm_s")
    if eca_psv and eca_psv > 150:
        findings.append("Elevated ECA PSV (>150 cm/s).")
    else:
        findings.append("Normal ECA PSV (<150 cm/s).")

    return findings

def classify_risk(findings:list[str]):
    text = " ".join(findings).lower()
    if "severe" in text:
        return "High"
    if "moderate" in text or "elevated" in text:
        return "Moderate"
    if "risk" in text or "increased" in text:
        return "Borderline"
    return "Normal"

