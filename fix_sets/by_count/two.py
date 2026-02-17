"""

python3 core8/pwb.py fix_sets/by_count/two ask

"""

import sys
from pathlib import Path
from api_bots import printe
from fix_sets.new import work_one_study
from fix_sets.by_count.bot import get_ids_o

if "st4" in sys.argv:
    from mass.st4.start import main_by_ids
Dir = Path(__file__).parent


def main():
    # ---
    ids_by_count2 = get_ids_o(2)
    # ---
    for n, (study_id, counts) in enumerate(ids_by_count2.items()):
        print(f"_____________\n {n=}/{len(ids_by_count2)}: {counts=}")
        if "st4" in sys.argv:
            main_by_ids([study_id])
        else:
            work_one_study(study_id)


if __name__ == "__main__":
    main()
