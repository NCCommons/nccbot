"""

from dup_sets.del_it import to_del_it

"""

from fix_sets.ncc_api import ncc_MainPage


def one(main_title, titles2):
    # ---
    text = f"\n\n== [[{main_title}]] ==\n"
    # ---
    for x in titles2:
        text += f"# [[{x}]]\n"
    # ---
    return text


def to_del_it(tab):
    # ---
    all_text = ""
    # ---
    for x, titles in tab.items():
        # ---
        text = one(x, titles)
        # ---
        all_text += text
    # ---
    page = ncc_MainPage("User:Mr._Ibrahem/Duplicate Radiopaedia sets", "www", family="nccommons")
    # ---
    page.save(newtext=all_text, summary="update", nocreate=0)
