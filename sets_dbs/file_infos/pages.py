"""

from sets_dbs.file_infos.pages import get_files


"""
import sys
import json
from pathlib import Path
from api_bots import printe
from api_bots.ncc_page import NEW_API

Dir = Path(__file__).parent

api_new = NEW_API()
# api_new.Login_to_wiki()

debug = "debug" in sys.argv
number = 10 if debug and "no" not in sys.argv else 500
len_all_files = 0


def dump_continues(params_continue):
    with open(Dir / "params_continue.json", "w", encoding="utf-8") as f:
        json.dump(params_continue, f, indent=2)

def one_rev(title, x):
    # ---
    return {
        "title": title,
        "parentid": x.get("parentid", ""),
        "content": x.get("slots", {}).get("main", {}).get("content", ""),
    }


def fetch_category_members(cat_title, params_continue=None):
    # get cat members
    # ---
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
    if params_continue:
        printe.output(f"<<blue>> add params_continue: len_all_files: {len_all_files}")
        dump_continues(params_continue)
        params.update(params_continue)
    # ---
    return api_new.post_params(params)


def process_category_data(data):
    global len_all_files
    # ---
    pages = data.get("query", {}).get("pages", [])
    # ---
    len_all_files += len(pages)
    # ---
    for page in pages:
        title = page["title"]
        # ---
        revisions = page.get("revisions", [{}])[0]
        # ---
        tab = one_rev(title, revisions)
        # ---
        yield tab


def get_files(params_continue=None):
    # ---
    # params[]"rvlimit"] = number # error: "titles", "pageids" or a generator was used to supply multiple pages, but the "rvlimit", "rvstartid", "rvendid", "rvdir=newer", "rvuser", "rvexcludeuser", "rvstart", and "rvend" parameters may only be used on a single page.
    # ---
    _result_example = {
        "batchcomplete": True,
        "continue": {"gcmcontinue": "file|...|3716402", "continue": "gcmcontinue||"},
        "query": {"pages": [{}]},
    }
    # ---
    cat_title = "Category:Uploads by Mr. Ibrahem"
    data = fetch_category_members(cat_title, params_continue)
    # ---
    error = data.get("error", {})
    # ---
    if error:
        printe.output(json.dumps(error, indent=2))
    # ---
    pages = data.get("query", {}).get("pages", [])
    # ---
    _pages_example = {
        "pageid": 3716253,
        "ns": 6,
        "revisions": [
            {
                "revid": 3777248,
                "parentid": 0,
                "timestamp": "2024-02-06T12:49:27Z",
                "slots": {"main": {"contentmodel": "wikitext", "contentformat": "text/x-wiki", "content": "== {{int:summary}} ==..."}},
            }
        ],
        "title": "File:État criblé with acute on chronic ischemia and amyloid angiopathy (Radiopaedia 35335-36839 Axial 3).jpg",
    }
    # ---
    yield from process_category_data(data)
    # ---
    if data.get("continue"):
        yield from get_files(data.get("continue", {}))
