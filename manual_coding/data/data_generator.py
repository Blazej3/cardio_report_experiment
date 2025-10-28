from pathlib import Path
import json, random, datetime

def one_record():
    def bounded(v,lo,hi):return max(lo, min(hi,v))

    cca_psv = random.uniform(50,150)
    ica_psv = bounded(cca_psv * random.uniform(0.9,2.5), 20, 300)
    eca_psv = random.uniform(40,200)

    patient_data ={
        "patient_id": "12345",
        "name": "adam cook",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "context": {"age_years": random.randint(18,90),
                    "sex": random.choice(["female", "male", "other", "unknown"]),
                    "notes": "Mock record"},
        "vitals": {
            "CCA": {
                "psv_cm_s": round(cca_psv,1), 
                "edv_cm_s": round(random.uniform(10,35),1), 
                "imt_mm": round(random.uniform(0.6,1.2),2)
                },

            "ICA":{
                "psv_cm_s": round(ica_psv,1), 
                "edv_cm_s": round(random.uniform(12,35),1), 
                "imt_mm": round(random.uniform(0.6,1.4),2)
                },

            "ECA": {
                "psv_cm_s": round(eca_psv,1), 
                "edv_cm_s": round(random.uniform(8,35),1), 
                    },
            "ica_cca_ratio": round(ica_psv/cca_psv,2)
        }
    }
    return patient_data
def main(out = "mock_patient.json"):
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    with open(out,"w", encoding="utf-8") as f:
        json.dump(one_record(),f, indent=2)
if __name__ == "__main__":
    main()
    