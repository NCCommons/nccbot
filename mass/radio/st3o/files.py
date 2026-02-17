"""

python3 core8/pwb.py mass/st3/files

tfj run files --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/st3/files"

"""

import re
from api_bots import printe
from api_bots.page_ncc import CatDepth
from mass.radio.lists.cases_to_cats import cases_cats  # cases_cats()
from mass.radio.bots.add_cat import add


def images_to_cats():
    members = CatDepth("Category:Radiopaedia_images_by_system", sitecode="www", family="nccommons", depth=1, ns="10")
    reg = r"^File:.*? \(Radiopaedia (\d+)\)\.\w+$"  # Match files with Radiopaedia case IDs
    # ---
    tab = {}
    # ---
    for file in members:
        match = re.match(reg, file)
        if match:
            case_id = match.group(1)
            # ---
            tab[file] = case_id
    # ---
    print(f"images_to_cats, length of members: {len(members)} ")
    print(f"images_to_cats, length of tab: {len(tab)} ")

    return tab


def start():
    # ---
    cats = cases_cats()
    imgs = images_to_cats()
    # ---
    new = {x: cats[v] for x, v in imgs.items() if v in cats}
    # ---
    print(f"{len(new)=}")
    for numb, (file, cat) in enumerate(new.items(), start=1):
        # ---
        printe.output(f"{file=}: {cat=}")
        # ---
        add(title=file, cat=cat)


if __name__ == "__main__":
    start()
