def interpret_vitals(patient:dict):
    
    findings = []
    vitals = patient.get("vitals")

    cca = vitals.get("CCA")
    ica = vitals.get("ICA")
    eca = vitals.get("ECA")
    ratio = vitals.get("ica_cca_ratio")
    
    ica_psv = ica.get("psv_cm_s")
    if ica_psv:
        if ica_psv > 200:
            findings.append("Severe ICA PSV, stenosis (>70%)")
        elif ica_psv > 125:
            findings.append("Moderate ICA PSV, stenosis (50-69%)")

    ica_edv = ica.get("edv_cm_s")
    if ica_edv:
        if ica_edv > 100:
            findings.append("Severe ICA EDV (>100 cm/s)")
        elif ica_edv > 40:
            findings.append("Moderate ICA EDV (40-100 cm/s)")
    ica_imt = ica.get("imt_mm")
    if ica_imt:
        if ica_imt >= 1.1:
            findings.append("Elevated ICA IMT (>1.0 mm)")
    
    cca_psv = cca.get("psv_cm_s")
    if cca_psv:
        if cca_psv > 125:
            findings.append("Elevated CCA PSV (>125 cm/s)")

    cca_edv = cca.get("edv_cm_s")
    if cca_edv:
        if cca_edv > 40:
            findings.append("Elevated CCA EDV (>40 cm/s)")
    cca_imt = cca.get("imt_mm")
    if cca_imt:
        if cca_imt >= 1.0:
            findings.append("Elevated CCA IMT (>1.0 mm)")

    eca_psv = eca.get("psv_cm_s")
    if eca_psv:
        if eca_psv > 150:
            findings.append("Elevated ECA PSV (>150 cm/s)")
    eca_edv = eca.get("edv_cm_s")
    if eca_edv:
        if eca_edv > 40:
            findings.append("Elevated ECA EDV (>40 cm/s)")
    
    if ratio:
        if ratio > 4.0:
            findings.append("Severe ICA/CCA suggests stenosis (>70%).")
        elif ratio > 2.0:
            findings.append("Elevated ICA/CCA suggest stenosis (>50%).")
        elif ratio > 1.5:
            findings.append("Mildly elevated ICA/CCA ratio.")

    return findings

def classify_risk(findings:list[str]):
    text = " ".join(findings).lower()
    if "severe" in text:
        return "High"
    if "moderate" in text or "elevated" in text or "mildly" in text:
        return "Moderate"
    return "Normal"



