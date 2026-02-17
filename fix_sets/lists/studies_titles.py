"""

python3 core8/pwb.py fix_sets/lists/studies_titles
python3 core8/pwb.py fix_sets/lists/studies_titles nodump
python3 core8/pwb.py fix_sets/lists/studies_titles nodump fix_2

Usage:
from fix_mass.files import studies_titles, study_to_case_cats


"""

import re
import sys
import json

from api_bots import printe
from fix_sets.ncc_api import CatDepth
from fix_sets.jsons_dirs import jsons_dir

mem_cach = {}


def get_members_ids(title):
    # ---
    members = CatDepth(title, sitecode="www", family="nccommons", depth=0, ns=0, onlyns=0)
    # ---
    not_match = 0
    title_to_id = {}
    # ---
    for x in members:
        # ---
        ma = re.match(r"^Radiopaedia case .*? id: \d+ study: (\d+)$", x)
        ma2 = re.match(r"^.*? \(Radiopaedia \d+-(\d+) .*?$", x)
        # ---
        set_id = ""
        # ---
        if ma:
            set_id = ma.group(1)
        elif ma2:
            set_id = ma2.group(1)
        else:
            not_match += 1
            continue
        # ---
        title_to_id[x] = set_id
    # ---
    printe.output(f"title: {title}")
    printe.output(f"\t title_to_id: {len(title_to_id):,}")
    printe.output(f"\t not_match: {not_match:,}")
    # ---
    return title_to_id


def get_mem(title):
    title_to_id = get_members_ids(title)
    # ---
    sets = {}
    duplicates = 0
    not_match = 0
    # ---
    for x, set_id in title_to_id.items():
        # ---
        if set_id in sets:
            duplicates += 1
            sets[set_id] = x
        else:
            sets[set_id] = x
    # ---
    printe.output(f"\t duplicates: {duplicates:,}")
    printe.output(f"\t{len(sets)=:,}")
    # ---
    mem_cach[title] = sets
    # ---
    return sets


def dumpit(file, data):
    file = jsons_dir / file
    # ---
    if "nodump" in sys.argv:
        return
    # ---
    # sort data
    data = dict(sorted(data.items(), key=lambda x: x[0]))
    # ---
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        printe.output(f"<<green>> write {len(data)} to file: {str(file)}")


def read_new(cat, file):
    # ---
    printe.output(f"read_new: {cat=}, {file=}")
    # ---
    file = jsons_dir / file
    # ---
    in_file = {}
    # ---
    # read file
    if file.exists():
        with open(file, "r", encoding="utf-8") as f:
            in_file = json.load(f)
            printe.output(f"<<green>> read {len(in_file)} from {file=}")
    # ---
    sets = get_mem(cat)
    # ---
    new_sets = {k: v for k, v in sets.items() if k not in in_file}
    # ---
    # merge the 2 dictionaries
    new_data = in_file.copy()
    new_data.update(new_sets)
    # ---
    printe.output(f"new_sets: {len(new_sets)}, in_file: {len(in_file)}, new_data: {len(new_data)}")
    # ---
    return new_data


def fix_2():
    # ---
    file1 = jsons_dir / "studies_titles.json"
    file2 = jsons_dir / "studies_titles2.json"
    # ---
    with open(file1, "r", encoding="utf-8") as f:
        data_1 = json.load(f)
        printe.output(f"<<green>> read {len(data_1)} from file1: {str(file1)}")
    # ---
    with open(file2, "r", encoding="utf-8") as f:
        data_2 = json.load(f)
        printe.output(f"<<green>> read {len(data_2)} from file2: {str(file2)}")
    # ---
    # items in data_2 and not in data_1
    new_data = {x: v for x, v in data_2.items() if x not in data_1}
    data_false = {x: v for x, v in data_2.items() if x in data_1}
    # ---
    printe.output(f"len(new_data): {len(new_data)}")
    # ---
    dumpit("studies_titles2.json", new_data)
    dumpit("studies_titles_false.json", data_false)


def main():
    cats_files = {
        "Category:Radiopaedia sets": "studies_titles.json",
        "Category:Image set": "studies_titles2.json",
    }
    # ---
    data_all = {}
    # ---
    for cat, file in cats_files.items():
        # ---
        data = read_new(cat, file)
        # ---
        data_all[file] = data
        # ---
        dumpit(file, data)
    # ---
    if "no_fix_2" not in sys.argv:
        fix_2()


if __name__ == "__main__":
    if "fix_2" in sys.argv:
        fix_2()
    else:
        main()
