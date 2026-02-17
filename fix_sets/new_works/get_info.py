"""

Usage:
from fix_sets.new_works.get_info import get_case_infos, get_study_infos

python3 core8/pwb.py fix_sets/new_works/get_info 90352
python3 core8/pwb.py fix_sets/new_works/get_info 109711
python3 core8/pwb.py fix_sets/new_works/get_info 101829

"""

import sys
import json
from mass.st3.One_x import OneCase
from mass.radio.jsons_bot import radio_jsons_dir
from fix_mass.files import study_id_to_case_id

with open(radio_jsons_dir / "all_ids.json", encoding="utf-8") as f:
    all_ids = json.load(f)

studies_cach = {}


def get_case_infos(caseId):
    # ---
    if caseId in studies_cach:
        return studies_cach[caseId]
    # ---
    va = all_ids.get(caseId)
    # ---
    if not va:
        print(f"no {caseId=} in all_ids")
        return {}
    # ---
    print(va)
    # {'url': 'https://radiopaedia.org/cases/forestier-disease', 'caseId': 90352, 'title': 'Forestier disease', 'studies': ['https://radiopaedia.org/cases/90352/studies/107656'], 'author': 'Subhan Iqbal', 'system': 'Musculoskeletal', 'published': '14 Jun 2021'}
    # ---
    caseId = va["caseId"]
    case_url = va["url"]
    author = va.get("author", "")
    title = va["title"]
    # ---
    studies = [study.split("/")[-1] for study in va["studies"]]
    # ---
    print("----------------- start: get_case_infos\n" * 2)
    # ---
    bot = OneCase(case_url, caseId, title, studies, author, work_dump_to_files=True)
    # ---
    result = bot.start_work_dump_to_files()
    # ---
    print("----------------- end: get_case_infos\n" * 2)
    # ---
    studies_cach[caseId] = result
    # ---
    return result


def get_study_infos(study_id):
    # ---
    caseId = study_id_to_case_id.get(study_id)
    # ---
    if not caseId:
        return {}
    # ---
    tab = get_case_infos(caseId)
    # ---
    result = tab.get(str(study_id), {})
    # ---
    return result


if __name__ == "__main__":
    ids = [arg.strip() for arg in sys.argv if arg.strip().isdigit()]
    # ---
    iinfos = get_case_infos(ids[0]) or get_study_infos(ids[0])
    # ---
    print(json.dumps(iinfos, indent=2))
