"""

python3 core8/pwb.py mass/radio/authors_list/auths_by_location
from mass.radio.authors_list.auths_by_location import locations
"""

import json
from pathlib import Path

import tqdm

import logging
logger = logging.getLogger(__name__)

main_dir = Path(__file__).parent
# ---
with open(main_dir / "authors_infos.json", "r", encoding="utf-8") as f:
    authors_infos = json.load(f)

locations = {}
# ---
for x, v in tqdm.tqdm(authors_infos.items()):
    # ---
    loc = v["location"].lower().strip()
    # split Los Angeles, United States to be United States
    # ---
    if "," in loc:
        loc = loc.split(",")[-1].strip()
    # ---
    locations.setdefault(loc, [])
    # ---
    v["name"] = x
    # ---
    locations[loc].append(v)
# ---
locations = dict(sorted(locations.items(), key=lambda x: len(x[1]), reverse=False))

def start() -> None:
    # ---
    for x, v in locations.items():
        x = x.title()
        logger.info(f"{x}: {len(v)}")

if __name__ == "__main__":
    start()
