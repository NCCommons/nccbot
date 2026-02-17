"""

from sets_dbs.file_infos.pages import get_files

python3 core8/pwb.py fix_db/file_infos/p2 debug

"""

import json
import logging
import sys
from pathlib import Path

from api_bots import printe
from api_bots.page_ncc import NEW_API

Dir = Path(__file__).parent
logger = logging.getLogger(__name__)
api_new = NEW_API()
# api_new.Login_to_wiki()

debug = "debug" in sys.argv
number = 10 if debug and "no" not in sys.argv else 500
len_all_files = {1: 0}


def dump_continues(params_continue):
    if debug:
        return
    try:
        with open(Dir / "params_continue.json", "w", encoding="utf-8") as f:
            json.dump(params_continue, f, indent=2)
    except Exception as e:
        logger.exception('Exception:', exc_info=True)


def get_continues():
    try:
        with open(Dir / "params_continue.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.exception('Exception:', exc_info=True)
        return {}


def printdebug(s):
    if debug:
        printe.output(s)


def one_rev(title, x):
    # ---
    return {
        "title": title,
        "parentid": x.get("parentid", ""),
        "content": x.get("slots", {}).get("main", {}).get("content", ""),
    }


def get_data(params_continue=None):
    # ---
    cat_title = "Category:Uploads by Mr. Ibrahem"
    # ---
    if params_continue:
        printe.output(f"<<blue>> add params_continue: len_all_files: {len_all_files[1]}")
        dump_continues(params_continue)
    # ---
    # get cat members
    params = {
        "action": "query",
        "format": "json",
        "prop": "pageprops|revisions",
        "generator": "categorymembers",
        "utf8": 1,
        "formatversion": "2",
        "rvprop": "content|ids|timestamp",
        "rvslots": "main",
        "rvdir": "older",
        "gcmtitle": cat_title,
        "gcmprop": "title",
        "gcmtype": "file",
        "gcmlimit": number,
        "gcmdir": "older",
    }
    # ---
    # params["rvlimit"] = number # error: "titles", "pageids" or a generator was used to supply multiple pages, but the "rvlimit", "rvstartid", "rvendid", "rvdir=newer", "rvuser", "rvexcludeuser", "rvstart", and "rvend" parameters may only be used on a single page.
    # ---
    max_do = 11
    pages = []
    # ---
    while params_continue or max_do == 11:
        # ---
        max_do -= 1
        # ---
        # printdebug(f"max_do:{max_do}")
        # ---
        if max_do == 0:
            break
        # ---
        if params_continue:
            params.update(params_continue)
        # ---
        data = api_new.post_params(params)
        # ---
        pages.extend(data.get("query", {}).get("pages", []))
        # ---
        error = data.get("error", {})
        # ---
        if error:
            printe.output(json.dumps(error, indent=2))
        # ---
        if data.get("continue"):
            params_continue = data["continue"]
        # ---
        del data
    # ---
    printdebug(f"len(pages): {len(pages)}")
    # ---
    len_all_files[1] += len(pages)
    # ---
    return pages, params_continue


def get_files(params_continue=None, load_json=False):
    # ---
    if load_json and not params_continue:
        params_continue = get_continues()
    # ---
    printdebug("get_files")
    # ---
    pages, continues = get_data(params_continue)
    # ---
    for page in pages:
        title = page["title"]
        # ---
        revisions = page.get("revisions", [{}])[0]
        # ---
        tab = one_rev(title, revisions)
        # ---
        yield tab
    # ---
    if continues:
        yield from get_files(continues)


def test():
    for x in get_files():
        pass


if __name__ == "__main__":
    test()
