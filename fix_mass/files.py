"""
from fix_mass.files import studies_titles, studies_titles2, study_to_case_cats, study_id_to_case_id
"""
import json
import os
from pathlib import Path

home_dir = os.getenv("HOME")
project = home_dir if home_dir else "I:/ncc"
jsons_dir = Path(project) / "ncc_jsons_dump/fix_mass_jsons"

studies_titles = {}
studies_titles2 = {}
study_to_case_cats = {}
study_id_to_case_id = {}
# ---
with open(jsons_dir / "studies_titles.json", "r", encoding="utf-8") as f:
    studies_titles = json.load(f)
    print(f"Loaded {len(studies_titles)} titles from 'studies_titles.json'.")
# ---
with open(jsons_dir / "studies_titles2.json", "r", encoding="utf-8") as f:
    studies_titles2 = json.load(f)
    print(f"Loaded {len(studies_titles2)} titles from 'studies_titles2.json'.")
# ---
with open(jsons_dir / "study_to_case_cats.json", "r", encoding="utf-8") as f:
    study_to_case_cats = json.load(f)
    print(f"Loaded {len(study_to_case_cats)} case categories from 'study_to_case_cats.json'.")
# ---
with open(jsons_dir / "study_id_to_case_id.json", "r", encoding="utf-8") as f:
    study_id_to_case_id = json.load(f)
    print(f"Loaded {len(study_id_to_case_id)} case IDs from 'study_id_to_case_id.json'.")
