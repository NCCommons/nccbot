"""
python3 core8/pwb.py mass/radio/st3sort/count_files/do nomult get:2323

tfj run update --mem 1Gi --image mariadb --command "$HOME/update.sh"
tfj run mnt2 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/st3sort/do get:2 "
tfj run mnt3 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/st3sort/do get:3 "
tfj run mnt4 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/st3sort/do get:4 "
tfj run mnt5 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/st3sort/do get:5 "
tfj run mnt6 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/st3sort/do get:6 "

python3 core8/pwb.py mass/radio/st3sort/do nomulti

"""
import os
import sys

sys.argv.append("dump_studies_urls_to_files")
import tqdm
import time
import json
from multiprocessing import Pool
from api_bots import printe
from pathlib import Path
from fix_mass.count_files.Case_co import CaseDo
from ncc_jsons.dir_studies_bot import studies_urls_to_files_dir
from mass.radio.jsons_bot import radio_jsons_dir

main_dir = Path(__file__).parent.parent.parent

def do_it(va):
    # ---
    caseId = va["caseId"]
    title = va["title"]
    studies = va["studies"]
    # ---
    bot = CaseDo(caseId, title, studies)
    bot.start()


def main(ids_tab):
    printe.output(f"<<purple>> start.py all: {len(ids_tab)}:")
    # ---
    tab = []
    # ---
    n = 0
    for _, va in tqdm.tqdm(ids_tab.items()):
        n += 1
        # ---
        caseId = va["caseId"]
        title = va["title"]
        studies = [study.split("/")[-1] for study in va["studies"]]
        # ---
        if not studies:
            printe.output(f"!!! studies not found: {caseId=}.")
            continue
        # ---
        tab.append({"caseId": caseId, "title": title, "studies": studies})
    # ---
    pool = Pool(processes=5)
    pool.map(do_it, tab)
    pool.close()
    pool.terminate()


def start():
    with open(radio_jsons_dir / "all_ids.json", encoding="utf-8") as f:
        all_ids = json.load(f)
    # ---
    ids_tab = {}
    # ---
    # all files in studies_urls_to_files_dir
    files = [x for x in os.listdir(studies_urls_to_files_dir) if x.endswith(".json")]
    # ---
    for file in files:
        print(file)
        break
    # ---
    for ii, va in tqdm.tqdm(all_ids.items()):
        # ---
        studies = [study.split("/")[-1] for study in va["studies"]]
        # ---
        new_s = []
        # ---
        if "dump_studies_urls_to_files" in sys.argv:
            for study in studies.copy():
                file = studies_urls_to_files_dir / f"{study}.json"
                if f"{study}.json" not in files:
                    new_s.append(study)
                # if os.path.exists(file):
                #     studies.remove(study)
        # ---
        if new_s:
            # ---
            ids_tab[ii] = va
    # ---
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxx")
    print(f"{len(ids_tab)=}, {len(all_ids)=}")
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxx")
    # ---
    time.sleep(3)
    # ---
    main(ids_tab)


if __name__ == "__main__":
    start()
