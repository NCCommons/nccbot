"""


tfj run --mem 1Gi onebot --image python3.9 --command "$HOME/nccbot/fix_mass/one_img_cat/u.sh"
tfj run --mem 1Gi onebot2 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_mass/one_img_cat/bot1 200"
tfj run --mem 1Gi onebot22 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_mass/one_img_cat/bot1 200 reverse"

python3 core8/pwb.py fix_mass/one_img_cat/bot1 from_files ask 1
python3 core8/pwb.py fix_mass/one_img_cat/bot1 files ask
python3 core8/pwb.py fix_mass/one_img_cat/bot1 ask

إضافة تصنيف إلى الصفحات التي بها صورة واحدة فقط

"""

import sys
from pathlib import Path
from api_bots import printe
from api_bots.page_ncc import ncc_MainPage
from api_bots.page_ncc import CatDepth

from fix_sets.bots2.filter_ids import filter_no_title

from fix_mass.one_img_cat.gt_files import from_files_g, work_get_files_data, count_files, count_files_true
from fix_mass.one_img_cat.lists import args_na

Dir = Path(__file__).parent


def update_text(title, MAIN_CAT_ONE, files=0):
    # ---
    printe.output(f"<<yellow>> update_text: {files=}")
    # ---
    page = ncc_MainPage(title)
    # ---
    p_text = page.get_text()
    new_text = p_text
    # ---
    for x in args_na.values():
        x_in = f"[[{str(x)}]]"
        if new_text.find(x_in) != -1:
            new_text = new_text.replace(x_in, "").strip()
    # ---
    new_text = new_text.strip()
    # ---
    if new_text.find(MAIN_CAT_ONE) == -1:
        new_text += f"\n[[{MAIN_CAT_ONE}]]"
    # ---
    if files == 1 and new_text.find("[[Category:Sort studies fixed]]") == -1 and new_text.count("|File:") == 1:
        new_text += "\n[[Category:Sort studies fixed]]"
    # ---
    if new_text.strip() == p_text.strip():
        printe.output("no changes..")
        return
    # ---
    page.save(newtext=new_text, summary=f"Added [[:{MAIN_CAT_ONE}]]")


def mk_ids_titles():
    ids_to_titles = {}
    # ---
    ids = from_files_g()
    # ---
    if not ids:
        ids = work_get_files_data()
    # ---
    ids_to_titles = filter_no_title(ids)
    # ---
    printe.output(f"<<yellow>> ids work_get_files_data: {len(ids):,}")
    printe.output(f"<<yellow>> ids from studies_titles: {len(ids_to_titles):,}")
    # ---
    print("work on count files:")
    # ---
    return ids_to_titles


def check_cat_page(MAIN_COUNT, MAIN_CAT_ONE):
    cat_page = ncc_MainPage(MAIN_CAT_ONE)
    # ---
    if not cat_page.exists():
        printe.output(f"<<red>> {MAIN_CAT_ONE} not exists")
        cat_page.Create(f"[[Category:Radiopaedia sets by number of images|{MAIN_COUNT}]]")


def do_titles(ids_titles, MAIN_COUNT, MAIN_CAT_ONE):
    # ---
    ids_titles = {k: v for k, v in ids_titles.items() if count_files_true(k, MAIN_COUNT)}
    # ---
    printe.output(f"<<yellow>> titles_only_one: {len(ids_titles):,}")
    printe.output(f"<<yellow>> titles_only_one: {len(ids_titles):,}")
    printe.output(f"<<yellow>> titles_only_one: {len(ids_titles):,}")
    # ---
    if not ids_titles:
        printe.output("<<red>> no ids_titles")
        return
    # ---
    pages_in = CatDepth(MAIN_CAT_ONE, sitecode="www", family="nccommons", depth=0, only_titles=True)
    # ---
    ids_titles = {s_id: s_t for s_id, s_t in ids_titles.items() if s_t not in pages_in.keys()}
    # ---
    printe.output(f"<<green>> ids_titles: {len(ids_titles):,}, after remove already_done..")
    # ---
    if not ids_titles:
        printe.output("<<red>> no ids_titles")
        return
    # ---
    return ids_titles


def main(ids_titles, MAIN_COUNT):
    # ---
    MAIN_CAT_ONE = args_na[MAIN_COUNT]
    # ---
    ids_titles = do_titles(ids_titles, MAIN_COUNT, MAIN_CAT_ONE)
    # ---
    if not ids_titles:
        printe.output("<<red>> no ids_titles")
        return
    # ---
    check_cat_page(MAIN_COUNT, MAIN_CAT_ONE)
    # ---
    # sort by key
    reverse = "r" in sys.argv or "reverse" in sys.argv
    # ---
    ids_titles = dict(sorted(ids_titles.items(), key=lambda item: item[1], reverse=reverse))
    # ---
    for n, (study_id, study_title) in enumerate(ids_titles.items()):
        # ---
        printe.output(f"page: {n}/{len(ids_titles):,}:")
        # printe.output(f"{study_id=}, {study_title=}")
        # ---
        all_files = count_files(study_id)
        # ---
        # printe.output(f"all_files: {all_files}")
        # ---
        # if all_files != MAIN_COUNT:
        if not count_files_true(study_id, MAIN_COUNT, counts=all_files):
            continue
        # ---
        update_text(study_title, MAIN_CAT_ONE, files=all_files)


def start():
    ta = []
    # ---
    if "all" in sys.argv:
        ta = list(args_na.keys())
    # ---
    if not ta:
        for x, ba in args_na.items():
            if str(x) in sys.argv:
                ta.append(x)
                printe.output(f"<<yellow>> MAIN_CAT_ONE: {ba}, MAIN_COUNT: {x}")
    # ---
    if not ta:
        ta = [1]
    # ---
    ids_to_titles = mk_ids_titles()
    # ---
    for x in ta:
        main(ids_to_titles, x)


if __name__ == "__main__":
    start()
