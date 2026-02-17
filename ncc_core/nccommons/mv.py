#!/usr/bin/python3
"""
python3 core8/pwb.py nccommons/mv
"""
import json
import sys

from pathlib import Path
from mdpy.bots import mdwiki_api
from api_bots.page_ncc import ncc_MainPage
from nccommons import api

import logging
logger = logging.getLogger(__name__)

Dir = str(Path(__file__).parents[0])
# print(f'Dir : {Dir}')
# ---
cats = {}
# ---
with open(f"{Dir}/mv.json", "r", encoding="utf-8") as f:
    cats = json.load(f)
# ---
logger.info(f"len of cats: {len(cats)}")
# ---
exists = {}

to_create = [x for x, t in exists.items() if t is False]
# ---
logger.info(f"len of to_create: {len(to_create)}")
# ---
for n, cat in enumerate(to_create, 1):
    logger.info(f"cat: {n}/{len(to_create)}:")
    text = mdwiki_api.GetPageText(cat)
    new = api.create_Page(text, cat, summary="Copy categories from mdwiki")
# ---
to_update = [x for x, t in exists.items() if t is True]
to_update = cats
# ---
# ---
n = 0


def delete_it(cat):
    # ---
    logger.info(f"cat: {n}/{len(to_update)}:")
    # ---
    params = {
        "action": "delete",
        "format": "json",
        "title": cat,
        "reason": "cat moved to nccommons.org",
    }  # , "deletetalk": 1}
    # ---
    doit = mdwiki_api.post_s(params, addtoken=True)
    # ---
    logger.info(f"doit: {doit}")


# ---
for cat in to_update:
    # ---
    n += 1
    # ---
    logger.info(f"cat: {n}/{len(to_update)}:")
    # ---
    nspage = ncc_MainPage(cat)
    # ---
    logger.info(f"GetPageText for page:{cat}")
    # ---
    md_text = mdwiki_api.GetPageText(cat)
    # ---
    if not md_text:
        continue
    # ---
    nc_text = nspage.get_text()
    # ---
    if md_text == nc_text:
        logger.info(f"{cat} is up to date")
    else:
        save_page = nspage.save(newtext=md_text, summary="Copy from mdwiki", nocreate=1)
    # ---
    delete_it(cat)
    # ---
    if "break" in sys.argv:
        break
    # ---
