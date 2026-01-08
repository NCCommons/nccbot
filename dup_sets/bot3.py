"""

python3 core8/pwb.py dup_sets/bot3
python3 core8/pwb.py dup_sets/bot3 multi del2
python3 core8/pwb.py dup_sets/bot3 multi del2 ask

لنقل الصفحات التي لا تحتوي على كلمة
Radiopaedia
من
Category:Image set
إلى
Category:Image stacks

"""

import sys
from api_bots import printe
from dup_sets.move_pages import move_them
from fix_sets.ncc_api import CatDepth


def main():
    # ---
    sets_o = CatDepth("Category:Image set", sitecode="www", family="nccommons", depth=0, onlyns=0)
    # ---
    sets = [x for x in sets_o if x.lower().find("radiopaedia") == -1]
    # ---
    printe.output(f"sets_o:{len(sets_o):,} \t sets without Radiopaedia: {len(sets):,}")
    # ---
    move_them(sets, old="Category:Image set", new="Category:Image stacks")


if __name__ == "__main__":
    main()
