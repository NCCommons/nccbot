"""

python3 core8/pwb.py fix_sets/by_count/co
python3 core8/pwb.py fix_sets/by_count/co titles2

from fix_sets.by_count.co import from_files, count_files
from fix_sets.by_count.co import files_file
"""
import sys
import json
import tqdm
from api_bots import printe
from pathlib import Path

from fix_sets.jsons_dirs import st_ref_infos
from fix_sets.lists.studies_fixed import studies_fixed_done
from fix_mass.files import studies_titles
from fix_sets.bots.stacks import get_stacks  # get_stacks(study_id)

Dir = Path(__file__).parent

files_file = Dir / "by_count.json"
# ---
if not files_file.exists():
    files_file.write_text("{}")
    data = {}
else:
    data = json.loads(files_file.read_text(encoding="utf-8"))


data_keys = list(data.keys())
data_keys.extend(studies_fixed_done)

data_keys = list(set(data_keys))


def count_files(x):
    file_js = st_ref_infos / x / "stacks.json"

    stacks = {}
    all_files = 0

    if file_js.exists():
        with open(file_js, "r", encoding="utf-8") as f:
            stacks = json.load(f)
    else:
        stacks = get_stacks(x)

    if stacks:
        # Combine loading and processing into a single expression (generator comprehension)
        public_filenames = {item["public_filename"] for item in stacks for item in item.get("images", [])}

        all_files = len(public_filenames)

    return all_files


def get_and_log(ids):
    ids = [x for x in ids if x not in data]

    newdata = {x: count_files(x) for x in ids}

    data.update(newdata)

    with open(files_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        printe.output(f"<<green>> write {len(data)} to {files_file=}")

    return data


def from_stacks_files():
    printe.output("from_stacks_files:")

    lala = []

    for subdir in tqdm.tqdm(st_ref_infos.iterdir(), total=80000):
        if not subdir.is_dir():
            continue

        study_id = subdir.name
        if study_id in data_keys:
            continue

        file_js = subdir / "stacks.json"

        if file_js.exists():
            lala.append(study_id)

    return lala


def from_titles2():
    # ---
    printe.output("from_titles2:")
    # ---
    titles2 = [x for x in studies_titles.keys() if x not in data_keys]
    # ---
    printe.output(f"from_titles2: {len(titles2):,}")
    # ---
    return titles2


def from_files():
    printe.output(f"co start: len data_keys: {len(data_keys)}")
    # ---
    if "titles2" in sys.argv:
        lala = from_titles2()
    else:
        lala = from_stacks_files()

    lal2 = []

    for study_id in tqdm.tqdm(lala):
        lal2.append(study_id)

        if len(lal2) == 5000:
            get_and_log(lal2)
            lal2 = []

    lisst_of_s = get_and_log(lal2)

    return lisst_of_s


if __name__ == "__main__":
    from_files()
