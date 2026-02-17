"""

from mass.st4.lists import authors, infos, all_ids, ids_by_caseId, authors_infos

"""

import sys
import json
from pathlib import Path

main_dir = Path(__file__).parent.parent
radio_jsons_dir = main_dir / "radio/jsons"
# ---
with open(main_dir / "radio/authors_list/authors_infos.json", encoding="utf-8") as f:
    authors_infos = json.load(f)
# ---
with open(radio_jsons_dir / "authors.json", encoding="utf-8") as f:
    authors = json.load(f)
# ---
with open(radio_jsons_dir / "infos.json", encoding="utf-8") as f:
    infos = json.load(f)
# ---
with open(radio_jsons_dir / "all_ids.json", encoding="utf-8") as f:
    all_ids = json.load(f)
# ---
# cases_in_ids = []
# ---
with open(radio_jsons_dir / "cases_in_ids.json", encoding="utf-8") as f:
    cases_in_ids = json.load(f)
# ---
ids_by_caseId = {x: v for x, v in all_ids.items() if x not in cases_in_ids}
# ---
if "allids" in sys.argv:
    ids_by_caseId = all_ids.copy()
# ---
print(f"{len(ids_by_caseId)=}, {len(cases_in_ids)=}")
# ---
del cases_in_ids
