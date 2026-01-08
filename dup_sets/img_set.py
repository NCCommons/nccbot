"""

python3 core8/pwb.py dup_sets/img_set multi del2 reverse

tfj run dup --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py dup_sets/img_set multi del2"

لإزالة الصفحات الموجودة في تصنيف
Category:Radiopaedia sets
وكذلك في تصنيف
Category:Image set

من التصنيف الثاني

"""
from api_bots import printe
from dup_sets.move_pages import move_them
from fix_sets.ncc_api import CatDepth


def maa():
    # ---
    Image_set = CatDepth("Category:Image set", sitecode="www", family="nccommons", depth=0, ns=0, onlyns=0)
    # ---
    print("++++++++++++++++++++++++++++")
    # ---
    cat2 = "Category:Radiopaedia sets"
    # ---
    sets_o = CatDepth(cat2, sitecode="www", family="nccommons", depth=0, ns=0, onlyns=0)
    # ---
    in_both_list = [x for x in sets_o if x in Image_set]
    # ---
    printe.output(f" len(in_both_list): {len(in_both_list):,}.")
    # ---
    move_them(in_both_list, old="Category:Image set", new=cat2)


if __name__ == "__main__":
    maa()
