"""

tfj run cdcd --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/st4/start noapi get:1 allids del2 updatetext"

tfj run allids --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/st4/start allids"

"""

import sys
import psutil
import tqdm
import os
from multiprocessing import Pool

from api_bots import printe
from mass.st4.One_x import OneCase
from mass.st4.lists import authors, infos, all_ids, ids_by_caseId, authors_infos


def print_memory():
    yellow, purple = "\033[93m%s\033[00m", "\033[95m%s\033[00m"

    usage = psutil.Process(os.getpid()).memory_info().rss
    usage = usage / 1024 // 1024

    print(yellow % "Memory usage:", purple % f"{usage} MB")


def do_it(va):
    # ---
    case_url = va["case_url"]
    caseId = va["caseId"]
    title = va["title"]
    studies = va["studies"]
    author = va["author"]
    # ---
    bot = OneCase(case_url, caseId, title, studies, author)
    bot.start()
    # ---
    del bot, author, title, studies


def multi_work(tab, numb=10):
    done = 0
    for i in range(0, len(tab), numb):
        group = tab[i : i + numb]
        # ---
        done += numb
        printe.output(f"<<purple>> done: {done}:")
        # ---
        print_memory()
        # ---
        if "nomulti" in sys.argv or "ask" in sys.argv or len(tab) < 10:
            for x in group:
                do_it(x)
        else:
            pool = Pool(processes=5)
            pool.map(do_it, group)
            pool.close()
            pool.terminate()


def ddo(taba):
    ids_tabs = taba
    tabs = {}
    print(f"all cases: {len(ids_tabs)}")
    length = (len(ids_tabs) // 6) + 1
    for i in range(0, len(ids_tabs), length):
        num = i // length + 1
        tabs[str(num)] = dict(list(ids_tabs.items())[i : i + length])
        # print(f'tab {num} : {len(tabs[str(num)])}')
        print(
            f'tfj run mnx{num} --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/st4/start get:{num} {len(tabs[str(num)])}"'
        )

    for arg in sys.argv:
        arg, _, value = arg.partition(":")
        if arg == "get":
            ids_tabs = tabs[value]
            print(f"work in {len(ids_tabs)} cases")
    del tabs

    return ids_tabs


def main(ids_tab):
    printe.output(f"<<purple>> start.py all: {len(ids_tab)}:")
    # ---
    print_memory()
    # ---
    if "test" not in sys.argv and len(ids_tab) > 100:
        ids_tab = ddo(ids_tab)
    # ---
    tab = []
    # ---
    n = 0
    for _, va in tqdm.tqdm(ids_tab.items()):
        n += 1
        # ---
        caseId = va["caseId"]
        case_url = va["url"]
        # ---
        author = va.get("author", "")
        # ---
        if not author:
            author = infos.get(case_url, {}).get(str(caseId), "")
        # ---
        if not author:
            author = authors.get(str(caseId), "")
        # ---
        title = va["title"]
        # ---
        studies = [study.split("/")[-1] for study in va["studies"]]
        # ---
        if not studies:
            printe.output(f"!!! studies not found: {caseId=}.")
            continue
        # ---
        tab.append({"caseId": caseId, "case_url": case_url, "title": title, "studies": studies, "author": author})
    # ---
    del ids_tab
    # ---
    multi_work(tab)


def main_by_ids(ids):
    printe.output(f"<<purple>> start.py main_by_ids: {len(ids)=}:")
    # ---
    ids_tab = {caseId: all_ids[caseId] for caseId in ids if caseId in all_ids}
    # ---
    not_in = [c for c in ids if c not in all_ids]
    # ---
    print(f"main_by_ids caseId not in all_ids: {len(not_in)}")
    # ---
    main(ids_tab)


if __name__ == "__main__":
    ids = [arg.strip() for arg in sys.argv if arg.strip().isdigit()]
    # ---
    ids = {x: all_ids[x] for x in ids if x in all_ids}
    # ---
    if ids:
        main(ids)
    else:
        main(ids_by_caseId)
