"""

from fix_sets.lists.studies_fixed import studies_fixed_done, studies_fixed_done

python3 core8/pwb.py fix_sets/lists/studies_fixed

"""

import tqdm
import os
import re
from pathlib import Path
from datetime import datetime

from fix_mass.helps_bot.file_bot import from_cach, dumpit
from fix_sets.ncc_api import CatDepth
from api_bots import printe

no_match = []

dd_file = Path(__file__).parent / "already_done.json"


def new_data():
    uu = []
    # ---
    jj = CatDepth(
        "Category:Sort studies fixed", sitecode="www", family="nccommons", depth=0, no_props=True, gcmlimit=5000
    )
    # ---
    for x in tqdm.tqdm(jj):
        # Regex to extract study IDs from categories
        pattern = r"\(Radiopaedia (\d+)-(\d+) "
        ma = re.search(pattern, x) or re.search(r"id: (\d+) study: (\d+)", x)
        if not ma:
            # Handle no matches explicitly
            no_match.append(x)
            continue
        # ---
        study_id = ma.group(2)
        # ---
        uu.append(study_id)
    # ---
    dumpit(uu, dd_file)
    # ---
    return uu


def get_data(mknew=False):
    # ---
    uu = from_cach(dd_file)
    # ---
    # Get the time of last modification
    last_modified_time = os.path.getmtime(dd_file)
    # ---
    date = datetime.fromtimestamp(last_modified_time).strftime("%Y-%m-%d")
    # ---
    today = datetime.today().strftime("%Y-%m-%d")
    # ---
    if date != today or not uu or mknew:
        printe.output(f"<<purple>> last modified: {date} , today: {today}, len: {len(uu)} ")
        uu = new_data()
    # ---
    return uu


studies_fixed_done = get_data()

print(f"studies_fixed_done: {len(studies_fixed_done):,}")

if __name__ == "__main__":
    get_data(mknew=True)
