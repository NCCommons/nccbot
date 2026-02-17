"""

tfj run catpages --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_mass/fix_sets/set_cats catpages"

python3 core8/pwb.py fix_mass/del_pages/bot ask
python3 core8/pwb.py fix_mass/del_pages/bot ask nocach

حذف صفحات الدراسات المكررة

"""

import re
import sys
from pathlib import Path

import tqdm

from api_bots.page_ncc import CatDepth
from fix_mass.helps_bot.file_bot import dumpit, from_cach
import logging
logger = logging.getLogger(__name__)

Dir = Path(__file__).parent

categories_by_title = {}

def one_study_titles(study_id, titles):
    # ---
    logger.info(f"<<yellow>> _____________\n {study_id=}, {len(titles)=}")
    # ---
    main_title = []
    # ---
    for x in titles:
        logger.info(f"# [[{x}]]")
        # ---
        categories = categories_by_title.get(x)
        # ---
        if "Category:Sort studies fixed" in categories:
            main_title.append(x)
    # ---
    logger.info(f"main_title: {main_title}")
    # ---
    return

def get_img_sets():
    cat1_file = Dir / "Category_Image_set.json"
    # ---
    cat1 = from_cach(cat1_file)
    # ---
    if not cat1:
        cat1 = CatDepth("Category:Image set", sitecode="www", family="nccommons", depth=0, props="categories")
        # cat1 = [title for title in cat1 if "Radiopaedia" in title]
        dumpit(cat1, cat1_file)
    # ---
    return cat1

def from_cat(cat1):
    # ---
    no_match = []
    # ---
    tab = {}
    # ---
    for title, ta in tqdm.tqdm(cat1.items()):
        # ---
        categories = ta.get("categories", [])
        # ---
        categories_by_title[title] = categories
        # ---
        # match text like [Appendicitis with localized perforation and abscess formation (Radiopaedia 49035-54130 A)]
        # match like [Radiopaedia case 2nd metatarsus stress fracture id: 175058 study: 141009]
        ma = re.search(r"\(Radiopaedia (\d+)-(\d+) ", title) or re.search(r"id: (\d+) study: (\d+)", title)
        if not ma:
            no_match.append(title)
            continue
        # ---
        study_id = ma.group(2)
        # ---
        tab.setdefault(study_id, [])
        # ---
        if title not in tab[study_id]:
            tab[study_id].append(title)
    # ---
    logger.info(f"no_match: {len(no_match)}, match: {len(tab)}")
    # ---
    return tab

def main():
    # ---
    cat1 = get_img_sets()
    # ---
    pages = from_cat(cat1)
    # ---
    max = 10 if "max" in sys.argv else 1
    # ---
    many_pages = {k: v for k, v in pages.items() if len(v) > max}
    # ---
    logger.info(f"All pages: {len(pages)}, study_id with many pages: {len(many_pages)}")
    # ---
    # sort many_pages by len of titles
    many_pages = {k: v for k, v in sorted(many_pages.items(), key=lambda item: len(item[1]), reverse=True)}
    # ---
    for study_id, titles in many_pages.items():
        one_study_titles(study_id, titles)

if __name__ == "__main__":
    main()
