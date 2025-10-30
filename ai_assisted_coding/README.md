# Cardio Report Generator (Non-Medical, Descriptive Only)

A tiny, local-only Python project that:
- Accepts input JSON (see `sample_data.json`) or generates mock data.
- Computes simple **descriptive** stats (min/max/mean) for PSV/EDV/IMT where present.
- Echoes `ica_cca_ratio` and flags the vessel with the highest PSV.
- Renders a readable HTML report and saves a PDF via WeasyPrint.
- Includes pytest-based tests.

> **Important**: This tool is **non-diagnostic** and **not a medical device**. Outputs are strictly descriptive.

## Requirements
- Python 3.12.7
- `pip install -r requirements.txt`
- WeasyPrint 66.0 requires system deps (e.g., Pango, Cairo). On Debian/Ubuntu:
  ```bash
  sudo apt-get update && sudo apt-get install -y libpango-1.0-0 libpangoft2-1.0-0 libcairo2 libffi8 libgdk-pixbuf-2.0-0
