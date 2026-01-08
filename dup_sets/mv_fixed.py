"""

python3 core8/pwb.py dup_sets/mv_fixed

tfj run dup --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py dup_sets/mv_fixed multi"

"""
import sys
import tqdm
from multiprocessing import Pool

from fix_sets.ncc_api import ncc_MainPage
from api_bots import printe
from fix_sets.ncc_api import CatDepth

# [[Category:Sort studies fixed]]
# [[Category:Image set]]


def rm_one(title):
    # ---
    old_cat = "[[Category:Image set]]"
    # ---
    page = ncc_MainPage(title)
    # ---
    if not page.exists():
        return
    # ---
    text = page.get_text()
    # ---
    newtext = text
    # ---
    if newtext.find("Category:Sort studies fixed") == -1:
        printe.output("page is not fixed..")
        return
    # ---
    if newtext.find("Category:Image set") != -1:
        newtext = newtext.replace(old_cat, "")
    # ---
    if newtext.find("[[Category:Radiopaedia sets]]") == -1 and newtext.find("[[Category:Radiopaedia sets|") == -1:
        newtext += "\n[[Category:Radiopaedia sets]]"
    # ---
    if newtext.strip() == text.strip():
        printe.output("no changes..")
        return
    # ---
    page.save(newtext=newtext, summary="Remove category")


def rm_titles(titles):
    # ---
    # move all titles from [[Category:Image set]] to [[Category:Duplicate Radiopaedia sets]]
    # ---
    printe.output(f"len(titles): {len(titles):,}")
    # ---
    if "multi" in sys.argv and "ask" not in sys.argv:
        pool = Pool(processes=4)
        pool.map(rm_one, titles)
        pool.close()
        pool.terminate()
    else:
        for title in tqdm.tqdm(titles):
            rm_one(title)


def main():
    # ---
    done1 = CatDepth("Category:Sort studies fixed", sitecode="www", family="nccommons", depth=0, ns=0, onlyns=0)
    done2 = CatDepth("Category:Image set", sitecode="www", family="nccommons", depth=0, ns=0, onlyns=0)
    # ---
    in_both = [title for title in done1 if title in done2]
    # ---
    printe.output(f" len(in_both): {len(in_both):,}.")
    # ---
    rm_titles(in_both)


if __name__ == "__main__":
    main()
