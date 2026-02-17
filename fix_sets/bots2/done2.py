"""

from fix_sets.bots2.done2 import filter_done, find_done_study #find_done_study(title)

python3 core8/pwb.py fix_sets/bots2/done2 printurl

"""

import json
import sys
from pathlib import Path

# from fix_mass.helps_bot.file_bot import from_cach, dumpit
from fix_sets.lists.studies_fixed import studies_fixed_done
import logging
logger = logging.getLogger(__name__)

def find_done_study(title):
    # ---
    if title in studies_fixed_done:
        return True
    # ---
    return False

def filter_done(ids_to_titles):
    # ---
    logger.info("filter_done::")
    # ---
    if "nodone" in sys.argv:
        return ids_to_titles
    # ---
    if not ids_to_titles:
        logger.info("\t<<red>> filter_done, no ids_to_titles. return {}")
        return ids_to_titles
    # ---
    already_done = [st_id for st_id in ids_to_titles.keys() if st_id in studies_fixed_done]
    # ---
    logger.info(f"already_done: {len(already_done):,}.")
    # ---
    if not already_done:
        return ids_to_titles
    # ---
    ids_to_titles = {st_id: study_title for st_id, study_title in ids_to_titles.items() if st_id not in already_done}
    # ---
    logger.info(f"<<green>> ids_to_titles: {len(ids_to_titles):,}, after remove already_done..")
    # ---
    return ids_to_titles

def filter_done_list(ids):
    # ---
    logger.info("filter_done_list::")
    # ---
    if "nodone" in sys.argv:
        return ids
    # ---
    if not ids:
        logger.info("\t<<red>> filter_done, no ids. return {}")
        return ids
    # ---
    if isinstance(ids, dict):
        ids = list(ids.keys())
    # ---
    already_done = [st_id for st_id in ids if st_id in studies_fixed_done]
    # ---
    logger.info(f"already_done: {len(already_done):,}.")
    # ---
    if not already_done:
        return ids
    # ---
    ids_new = [k for k in ids if k not in already_done]
    # ---
    logger.info(f"<<green>> ids_new: {len(ids_new):,}, after remove already_done..")
    # ---
    return ids_new

if __name__ == "__main__":
    file_path = Path(__file__).parent / "x.json"
    title = "Acute pancreatic necrosis (Radiopaedia 13560-18500 Axial C+ portal venous phase)"
    print(find_done_study(title))
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(studies_fixed_done, f, indent=2)
