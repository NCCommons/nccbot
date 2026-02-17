"""

python3 core8/pwb.py dup_sets/bot

tfj run dup --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py dup_sets/bot multi"

إيحاد الصفحات المكررة ثم إضافتها إلى تصنيف:
Category:Duplicate Radiopaedia sets

وايجاد الصفحات المكررة عن صفحات تم إصلاحها وإضافتها إلى تصنيف:
Category:To delete
"""

# import re
# import sys

import tqdm
import json

from api_bots import printe
from fix_sets.jsons_dirs import jsons_dir
from dup_sets.get_mem import get_all_titles
from dup_sets.move_pages import move_titles
from dup_sets.del_it import to_del_it
from fix_sets.ncc_api import CatDepth

fixed = CatDepth("Category:Sort studies fixed", sitecode="www", family="nccommons", depth=0, ns=0, onlyns=0)


def dumpit(file, data):
    file = jsons_dir / file
    # ---
    # sort data
    data = dict(sorted(data.items(), key=lambda x: x[0]))
    # ---
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        printe.output(f"<<green>> write {len(data)} to file: {str(file)}")


def read_files():
    # ---
    file1 = jsons_dir / "studies_titles.json"
    file2 = jsons_dir / "studies_titles2.json"
    # ---
    with open(file1, "r", encoding="utf-8") as f:
        data_1 = json.load(f)
    # ---
    with open(file2, "r", encoding="utf-8") as f:
        data_2 = json.load(f)
    # ---
    # items in data_2 and not in data_1
    new_data = {x: v for x, v in data_2.items() if x not in data_1}
    # ---
    all_data = data_1.copy()
    all_data.update(new_data)
    # ---
    return all_data


def move_them(to_move, old="", new=""):
    # ---
    if len(to_move) == 0:
        return
    # ---
    done = CatDepth(new, sitecode="www", family="nccommons", depth=0, ns=0, onlyns=0)
    # ---
    new_to_move = [x for x in to_move if x not in done]
    # ---
    printe.output(f" len(to_move): {len(to_move):,}, after done : {len(new_to_move):,}")
    # ---
    move_titles(new_to_move, old, new)


def main():
    # ---
    all_data_valid = read_files()
    # ---
    ids_to_title = get_all_titles(cache=True)
    # ---
    printe.output(f"len(all_data_valid): {len(all_data_valid):,}")
    # ---
    printe.output(f"len(ids_to_title): {len(ids_to_title):,}")
    # ---
    # filter only x_id with 2 or more titles
    more_one = {k: v for k, v in ids_to_title.items() if len(v) > 1}
    # ---
    more_one = {k: v for k, v in sorted(more_one.items(), key=lambda item: len(item[1]), reverse=True)}
    # ---
    printe.output(f" len(more_one): {len(more_one)}")
    to_del = []
    to_del_pp = {}
    to_move = []
    # ---
    for study_id, titles in tqdm.tqdm(more_one.items()):
        # ---
        main_title = all_data_valid.get(study_id)
        # ---
        if not main_title:
            continue
        # ---
        titles2 = [x for x in titles if x != main_title]
        # ---
        if main_title in fixed:
            to_del_pp[main_title] = titles2
            to_del.extend(titles2)

        elif main_title in titles:
            to_move.extend(titles2)
    # ---
    printe.output(f" len(to_del): {len(to_del)}")
    printe.output(f" len(to_move): {len(to_move)}")
    # ---
    move_them(to_move, old="Category:Image set", new="Category:Duplicate Radiopaedia sets")
    # ---
    printe.output(f" len main_title in fixed: {len(to_del_pp)}")
    # ---
    move_them(to_del, old="Category:Duplicate Radiopaedia sets", new="Category:To delete")
    # ---
    to_del_it(to_del_pp)


if __name__ == "__main__":
    main()
