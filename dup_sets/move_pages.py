"""

python3 core8/pwb.py fix_sets/dup_sets

from dup_sets.move_pages import move_titles
"""

import tqdm
import sys
from multiprocessing import Pool

from api_bots import printe
from fix_sets.ncc_api import ncc_MainPage, CatDepth

len_all = {1: 0}


def del_cat(newtext, old):
    # ---
    old_cat = f"[[{old}]]"
    # ---
    if newtext.find(f"[[{old}") == -1:
        return newtext
    # ---
    if newtext.find(old_cat) != -1:
        newtext = newtext.replace(old_cat, "")
        return newtext
    # ---
    if newtext.find(f"[[{old}|") != -1:
        for x in newtext.split("\n"):
            if x.find(f"[[{old}|") != -1:
                newtext = newtext.replace(x, "")
        return newtext
    # ---
    return newtext


def move_one(taa):
    # ---
    title, old, new, number = taa
    # ---
    old = old.replace("_", " ")
    new = new.replace("_", " ")
    # ---
    new_cat = f"[[{new}]]"
    # ---
    page = ncc_MainPage(title)
    # ---
    if not page.exists():
        return
    # ---
    summary = "Add category"
    # ---
    text = page.get_text()
    # ---
    text = text.replace(old.replace(" ", "_"), old)
    text = text.replace(new.replace(" ", "_"), new)
    # ---
    has_new = False
    # ---
    if text.find(f"[[{new}]]") != -1 or text.find(f"[[{new}|") != -1:
        has_new = True
        # ---
        if "del2" not in sys.argv:
            printe.output(f"[[{new}]] already in {title}")
            return
    # ---
    newtext = text
    # ---
    newtext = del_cat(newtext, old)
    # ---
    if has_new and text == newtext:
        printe.output(f"page ({title}) has_new and hasn't old ")
        return
    # ---
    if not has_new:
        newtext += f"\n{new_cat}"
        summary = f"Add category [[:{new}]]"
    else:
        summary = f"Remove category [[:{old}]]"
    # ---
    if newtext.strip() == text.strip():
        printe.output("no changes..")
        return
    # ---
    nm = 100
    nm = len_all[1] // 20
    # ---
    if nm == 0:
        nm = 10
    # ---
    if number % nm == 0 or number < 10:
        printe.output(f"<<yellow>> {number}/{len_all[1]:,} DONE....")
    # ---
    page.save(newtext=newtext, summary=summary)


def move_titles(titles, old, new):
    # ---
    # move all titles from [[Category:Image set]] to [[Category:Duplicate Radiopaedia sets]]
    # ---
    len_all[1] = len(titles)
    # ---
    if "reverse" in sys.argv:
        titles = list(reversed(titles))
    # ---
    printe.output(f"len(titles): {len(titles):,}")
    # ---
    if "multi" in sys.argv and "ask" not in sys.argv:
        titles = [[x, old, new, number] for number, x in enumerate(titles)]
        pool = Pool(processes=4)
        pool.map(move_one, titles)
        pool.close()
        pool.terminate()
    else:
        for number, title in tqdm.tqdm(enumerate(titles)):
            move_one([title, old, new, number])


def move_them(to_move, old="", new=""):
    # ---
    if len(to_move) == 0:
        return
    # ---
    done = []
    # ---
    if "del2" not in sys.argv:  # or len(to_move) < 20:
        done = CatDepth(new, sitecode="www", family="nccommons", depth=0, ns=0, onlyns=0)
    # ---
    new_to_move = [x for x in to_move if x not in done]
    # ---
    printe.output(f" len(to_move): {len(to_move):,}, after done : {len(new_to_move):,}")
    # ---
    move_titles(new_to_move, old, new)
