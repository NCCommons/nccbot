"""

from fix_mass.one_img_cat.gt_files import from_files_g, work_get_files_data, count_files, count_files_true

"""

import json
from pathlib import Path

import tqdm
from api_bots import printe
from fix_mass.one_img_cat.lists import args_na_more
from fix_sets.bots.stacks import get_stacks
from fix_sets.by_count.lists import counts_from_files
from fix_sets.jsons_dirs import st_ref_infos

Dir = Path(__file__).parent

count_cach = {}


def count_files(study_id):
    # ---
    study_id = str(study_id)
    # ---
    if count_cach.get(study_id):
        return count_cach[study_id]
    # ---
    stacks_data = get_stacks(study_id)
    # ---
    all_files = []
    # ---
    for x in stacks_data:
        all_files.extend([x["public_filename"] for x in x["images"]])
    # ---
    all_files = list(set(all_files))
    # ---
    count_cach[study_id] = len(all_files)
    # ---
    return len(all_files)


def count_files_true(k, main_number, counts=False):
    # ---
    if not counts:
        counts = count_files(k)
    # ---
    if main_number in args_na_more:
        if counts >= main_number and counts < args_na_more[main_number]:
            return True
    else:
        if counts == main_number:
            return True
    # ---
    return False


def from_files_g():
    # ---
    files_file = Dir / "studies_one_file.json"
    # ---
    if not files_file.exists():
        files_file.write_text("{}")
    # ---
    try:
        with open(files_file, "r", encoding="utf-8") as f:
            lisst_of_s = json.load(f)
    except Exception as e:
        printe.output(f"<<red>> Error reading {files_file}: {str(e)}")
        return False
    # ---
    # counts_from_files
    # ---
    lisst_of_s.update(counts_from_files())
    # ---
    if lisst_of_s:
        for x, counts in lisst_of_s.items():
            count_cach[x] = counts
    # ---
    lisst_of_s = list(lisst_of_s.keys())
    # ---
    return lisst_of_s


def work_get_files_data():
    # ---
    lisst_of_s = []
    # ---
    for subdir in tqdm.tqdm(st_ref_infos.iterdir(), total=80000):
        # ---
        if not subdir.is_dir():
            continue
        # ---
        study_id = subdir.name
        # ---
        file_js = subdir / "stacks.json"
        # ---
        if not file_js.exists():
            continue
        # ---
        lisst_of_s.append(study_id)
    # ---
    files_file = Dir / "studies_one_file.json"
    # ---
    if not files_file.exists():
        files_file.write_text("[]")
    # ---
    with open(files_file, "w", encoding="utf-8") as f:
        json.dump(lisst_of_s, f, ensure_ascii=False, indent=2)
    # ---
    return lisst_of_s


if __name__ == "__main__":
    # python3 core8/pwb.py fix_mass/one_img_cat/gt_files
    # ---
    fos = [
        ("", 100, 200),
        ("", 100, 100),
        ("", 200, 100),
        ("", 200, 200),
    ]
    # ---
    for _, ma, counts in fos:
        print(f"{ma=}, {counts=}")
        print(count_files_true("", ma, counts=counts))
