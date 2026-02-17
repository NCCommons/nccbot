"""

python3 core8/pwb.py fix_sets/dup_sets

from dup_sets.get_mem import get_all_titles
"""

import json
import re
from pathlib import Path

from api_bots import printe
from fix_sets.ncc_api import CatDepth


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


def dumpit(file, data):
    # ---
    # sort data
    data = dict(sorted(data.items(), key=lambda x: x[0]))
    # ---
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        printe.output(f"<<green>> write {len(data)} to file: {str(file)}")


def new_get_all_titles():
    # ---
    data_all = {}
    # ---
    title_to_id1 = get_members_ids("Category:Radiopaedia sets")
    title_to_id2 = get_members_ids("Category:Image set")
    # ---
    title_to_id1.update(title_to_id2)
    # ---
    for title, x_id in title_to_id1.items():
        # ---
        data_all.setdefault(x_id, [title])
        # ---
        if title not in data_all[x_id]:
            data_all[x_id].append(title)
    # ---
    return data_all


def get_all_titles(cache=False):
    file = Path(__file__).parent / "all_members.json"
    # ---
    if cache and file.exists():
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    # ---
    titles = new_get_all_titles()
    # ---
    dumpit(file, titles)
    # ---
    return titles
