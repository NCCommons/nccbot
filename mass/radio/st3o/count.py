"""

python3 core8/pwb.py mass/st3/count

tfj run coca --image python3.9 --command "$HOME/local/bin/python3 c8/pwb.py mass/radio/cases_in_ids && $HOME/local/bin/python3 c8/pwb.py mass/st3/count"

"""
import json
import os
import tqdm
import sys
from datetime import datetime

from mass.radio.get_studies import get_images, get_images_stacks
from api_bots.ncc_page import ncc_MainPage

from ncc_jsons.dir_studies_bot import studies_dir
from mass.radio.jsons_bot import radio_jsons_dir


with open(radio_jsons_dir / "all_ids.json", encoding="utf-8") as f:
    all_ids = json.load(f)

with open(radio_jsons_dir / "cases_in_ids.json", encoding="utf-8") as f:
    cases_in_ids = json.load(f)
# ---
ids_tab = {x: v for x, v in all_ids.items() if x not in cases_in_ids}

cases_done = len(all_ids) - len(ids_tab)


class All:
    cases = 0
    images = 0
    studies = 0


All.cases = len(ids_tab)
cases_count_file = radio_jsons_dir / "cases_count.json"


def cases_counts():
    if not os.path.exists(cases_count_file):
        with open(cases_count_file, "w", encoding="utf-8") as f:
            f.write("{}")

    try:
        with open(cases_count_file, encoding="utf-8") as f:
            cases_count = json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error reading {cases_count_file}: {e}")
        return {}


    return cases_count


def get_studies(studies_ids, caseId):
    print(f"get_studies {caseId=}")
    images_count = 0
    for study in studies_ids:
        st_file = studies_dir / f"{study}.json"
        images = {}
        if os.path.exists(st_file):
            try:
                with open(st_file, encoding="utf-8") as f:
                    images = json.load(f)
            except Exception as e:
                print(f"{study} : error")
        images = [image for image in images if image]
        if not images:
            images = get_images_stacks(caseId)
        if not images:
            url = f"https://radiopaedia.org/cases/{caseId}/studies/{study}"
            images = get_images(url)
        images_count += len(images)

    return images_count


def sa():
    day = datetime.now().strftime("%Y-%b-%d %H:%M:%S")
    # text = f"{day}\n"
    text = "* --~~~~\n"

    text += f"* All Cases: {len(all_ids):,}\n"
    text += f"* Cases done: {cases_done:,}\n\n"
    text += ";Remaining:\n"
    text += f"* Cases: {All.cases:,}\n"
    text += f"* Images: {All.images:,}\n"
    text += f"* Studies: {All.studies:,}\n"

    print(text)

    page = ncc_MainPage("User:Mr. Ibrahem/Radiopaedia", "www", family="nccommons")

    if page.exists():
        page.save(newtext=text, summary="update")
    else:
        page.Create(text=text, summary="update")


def start():
    images_count = cases_counts()
    print(f"{len(images_count)=}")
    # ---
    print(f"<<purple>> start.py all: {len(ids_tab)}:")
    # ---
    for n, (_, va) in enumerate(tqdm.tqdm(ids_tab.items()), 1):
        caseId = va["caseId"]

        studies = [study.split("/")[-1] for study in va["studies"]]
        All.studies += len(studies)
        da = images_count.get(caseId) or images_count.get(str(caseId))
        if da:
            images = da
        else:
            images = get_studies(studies, caseId)
            images_count[caseId] = images

        All.images += images

        if "test" in sys.argv and n == 100:
            break

    sa()

    with open(cases_count_file, "w", encoding="utf-8") as f:
        json.dump(images_count, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    start()
