"""


tfj run cdcf --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_mass/one_img_cat/skiped"

python3 core8/pwb.py fix_mass/one_img_cat/skiped from_files ask
python3 core8/pwb.py fix_mass/one_img_cat/skiped files ask
python3 core8/pwb.py fix_mass/one_img_cat/skiped ask

العمل على المقالات التي بها صورة واحدة فقط

"""

# import re
import sys
from pathlib import Path

from api_bots import printe
from api_bots.page_ncc import ncc_MainPage
from fix_mass.files import studies_titles
from fix_mass.one_img_cat.gt_files import count_files, from_files_g, work_get_files_data
from fix_sets.bots2.done2 import filter_done_list
from fix_sets.bots2.filter_ids import filter_no_title
from fix_sets.bots2.text_cat_bot import add_cat_to_set

Dir = Path(__file__).parent


def update_text(title, study_id):
    # ---
    printe.output(f"<<yellow>> update_text: {title}")
    # ---
    page = ncc_MainPage(title)
    # ---
    p_text = page.get_text()
    new_text = p_text
    # ---
    if new_text.find("Category:Sort studies fixed") == -1:
        new_text += "\n[[Category:Sort studies fixed]]"
    # ---
    if new_text.find("[[Category:Radiopaedia case ") == -1:
        new_text = add_cat_to_set(new_text, study_id, title)
    # ---
    if new_text.strip() == p_text.strip():
        printe.output("no changes.., page has [[Category:Sort studies fixed]]..")
        return
    # ---
    page.save(newtext=new_text, summary="Added [[:Category:Sort studies fixed]]")


def one_st(study_id, study_title):
    # ---
    all_files = count_files(study_id)
    # ---
    printe.output(f"all_files: {all_files}")
    # ---
    if all_files > 1:
        return False
    # ---
    update_text(study_title, study_id)


def get_ids():
    if "from_files" in sys.argv:
        ids = from_files_g()
        printe.output(f"<<yellow>> ids from_files: {len(ids):,}")
        return ids
    # ---
    if "files" in sys.argv:
        ids = work_get_files_data()
        printe.output(f"<<yellow>> ids files: {len(ids):,}")
        return ids
    # ---
    ids = list(studies_titles.keys())
    printe.output(f"<<yellow>> ids from studies_titles: {len(ids):,}")
    return ids


def main(ids):
    # ---
    if not ids:
        ids = get_ids()
    # ---
    ids = filter_done_list(ids)
    # ---
    ids_to_titles = filter_no_title(ids)
    # ---
    ids_to_titles = {k: v for k, v in ids_to_titles.items() if count_files(k) == 1}
    # ---
    printe.output(f"<<yellow>> titles_only_one: {len(ids_to_titles):,}")
    printe.output(f"<<yellow>> titles_only_one: {len(ids_to_titles):,}")
    printe.output(f"<<yellow>> titles_only_one: {len(ids_to_titles):,}")
    # ---
    for n, (study_id, study_title) in enumerate(ids_to_titles.items(), 1):
        printe.output("_____________________________")
        printe.output(f"<<yellow>> {n:,}/{len(ids_to_titles):} {study_id=}, {study_title=}")
        # ---
        one_st(study_id, study_title)


if __name__ == "__main__":
    ids = [arg.strip() for arg in sys.argv if arg.strip().isdigit()]
    # ---
    main(ids)
