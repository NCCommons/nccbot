"""

يعمل هذا البوت على إضافة تصنيف لجميع الصفحات التابعة للكتاب الأمريكيين

python3 core8/pwb.py mass/radio/authors_list/usa_sets ask

tfj run ussets --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/authors_list/usa_sets"

"""

import json
import sys
from multiprocessing import Pool
from pathlib import Path

import tqdm
from api_bots import printe
from api_bots.page_ncc import NEW_API, CatDepth
from fix_mass.files import studies_titles, studies_titles2
from mass.radio.authors_list.auths_by_location import locations
from mass.radio.jsons_bot import radio_jsons_dir

studies_titles.update(studies_titles2)

United_States = locations.get("united states", [])

main_dir = Path(__file__).parent.parent

with open(radio_jsons_dir / "all_ids.json", "r", encoding="utf-8") as f:
    all_ids = json.load(f)
# ---
with open(main_dir / "authors_list" / "authors_to_cases.json", "r", encoding="utf-8") as f:
    authors_to_cases = json.load(f)

api_new = NEW_API()


def get_studies_of_cases(cases: list) -> list:
    """
    get sets of images
    """
    sets = []
    # ---
    for x in cases:
        va = all_ids.get(x)
        # ---
        if not va:
            continue
        # ---
        studies = [study.split("/")[-1] for study in va["studies"]]
        # ---
        sets.extend(studies)
    # ---
    return sets


def add_it(title):
    text = "\n[[Category:Radiopaedia studies by United States authors]]"
    # ---
    api_new.Add_To_Bottom(text, "Added category", title, poss="Bottom")


def add_cat_to_all_studies(titles: list) -> None:
    # ---
    if "multi" in sys.argv and "ask" not in sys.argv:
        pool = Pool(processes=3)
        pool.map(add_it, titles)
        pool.close()

        pool.terminate()
    else:
        for title in tqdm.tqdm(titles):
            add_it(title)


def get_auth_to_studies() -> None:
    # ---
    list_of_auths = [x["name"] for x in United_States]
    # ---
    auths_by_cases = {x: authors_to_cases.get(x, []) for x in list_of_auths}
    # ---
    auths_by_cases = dict(sorted(auths_by_cases.items(), key=lambda x: len(x[1]), reverse=False))
    # ---
    tab = {}
    # ---
    for n, (auth, cases) in enumerate(auths_by_cases.items(), start=1):
        # ---
        studies = get_studies_of_cases(cases)
        # # ---
        # print(f"{n}/{len(auths_by_cases.items())}\t cases={len(cases)}\t studies={len(studies)}\t {auth=}")
        # ---
        tab[auth] = studies
    # ---
    tab = dict(sorted(tab.items(), key=lambda x: len(x[1]), reverse=False))
    # ---
    return tab


def get_titles(tab):
    all_studies = []
    # ---
    for n, (auth, studies) in enumerate(tab.items(), start=1):
        # ---
        print(f"{n}/{len(tab.items())}\t studies = {len(studies)}\t {auth=}")
        # ---
        all_studies.extend(studies)
    # ---
    all_studies = list(set(all_studies))
    # ---
    printe.output(f"all_studies: {len(all_studies)}")
    # ---
    titles = [studies_titles.get(study) for study in all_studies if studies_titles.get(study)]
    # ---
    studies_no_titles = [x for x in all_studies if not studies_titles.get(x)]
    # ---
    printe.output(f"titles: {len(titles)}, studies_no_titles: {len(studies_no_titles)}")
    # ---
    return titles


def start() -> None:
    # ---
    tab = get_auth_to_studies()
    # ---
    titles = get_titles(tab)
    # ---
    done = CatDepth(
        "Category:Radiopaedia studies by United States authors", sitecode="www", family="nccommons", depth=0, ns=""
    )
    # ---
    new_titles = [x for x in titles if x not in done]
    # ---
    printe.output(f"titles done: {len(done):,}\t new_titles: {len(new_titles):,}")
    # ---
    add_cat_to_all_studies(new_titles)


if __name__ == "__main__":
    start()
