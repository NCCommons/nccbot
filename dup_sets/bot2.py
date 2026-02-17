"""

python3 core8/pwb.py dup_sets/bot2
python3 core8/pwb.py dup_sets/bot2 nodone
python3 core8/pwb.py dup_sets/bot2 multi fi del2
python3 core8/pwb.py dup_sets/bot2 multi to_do del2
python3 core8/pwb.py dup_sets/bot2 multi in_both del2 ask DermNet

لنقل الصفحات
من تصنيف
Category:Image set

إلى تصنيفات فرعية موجودة داخل تصنيف

Category:Image stacks

"""

import sys

from dup_sets.move_pages import move_them
from fix_sets.ncc_api import CatDepth
import logging
logger = logging.getLogger(__name__)

lal = [
    "GovernmentZA",
    "DermNet",
    "Atlasdermatologico",
    "EyeRounds",
    "UndergradImaging",
    "USAID",
]
# ---
for x in lal[:]:
    if x in sys.argv:
        lal = [x]
        break

def in_both():
    # ---
    Image_set = CatDepth("Category:Image set", sitecode="www", family="nccommons", depth=0, ns=0, onlyns=0)
    # ---
    for cat in lal:
        print("++++++++++++++++++++++++++++")
        # ---
        cat2 = f"Category:{cat} sets"
        # ---
        sets_o = CatDepth(cat2, sitecode="www", family="nccommons", depth=0, ns=0, onlyns=0)
        # ---
        in_both_list = [x for x in sets_o if x in Image_set]
        # ---
        logger.info(f" len(in_both_list): {len(in_both_list):,}.")
        # ---
        move_them(in_both_list, old="Category:Image set", new=cat2)

def to_do():
    # ---
    Image_set = CatDepth("Category:Image set", sitecode="www", family="nccommons", depth=0, ns=0, onlyns=0)
    # ---
    for cat in lal:
        print("++++++++++++++++++++++++++++")
        # ---
        cat2 = f"Category:{cat} sets"
        # ---
        to_do_list = [x for x in Image_set if x.lower().find(cat.lower()) != -1]
        # ---
        logger.info(f" len(to_do_list): {len(to_do_list):,}.")
        # ---
        move_them(to_do_list, old="Category:Image set", new=cat2)

def main():
    # ---
    Image_set = CatDepth("Category:Image set", sitecode="www", family="nccommons", depth=0, ns=0, onlyns=0)
    # ---
    for cat in lal:
        # ---
        print("++++++++++++++++++++++++++++")
        # ---
        sets_o = CatDepth(f"Category:{cat}", sitecode="www", family="nccommons", depth=0, ns=14, onlyns=14)
        # ---
        ssets = [title.replace("Category:", "") for title in sets_o]
        # ---
        if f"{cat} sets" in ssets:
            ssets.remove(f"{cat} sets")
        # ---
        logger.info(f" len(ssets): {len(ssets):,}.")
        # ---
        if "fi" in sys.argv:
            ssets = [x for x in ssets if x in Image_set]
            logger.info(f" filter only page in Category:Image set: {len(ssets):,}.")
        # ---
        move_them(ssets, old="Category:Image set", new=f"Category:{cat} sets")

if __name__ == "__main__":
    if "in_both" in sys.argv:
        in_both()
    elif "to_do" in sys.argv:
        to_do()
    else:
        main()
