"""

python3 core8/pwb.py fix_sets/by_count/bot ask

tfj run byc2 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_sets/by_count/bot hasskip 2"
tfj run byc3 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_sets/by_count/bot hasskip 3"
tfj run byc4 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_sets/by_count/bot hasskip 4"
tfj run byc5 --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py fix_sets/by_count/bot hasskip 5"
$HOME/local/bin/python3 core8/pwb.py fix_sets/by_count/bot hasskip 8 ask

"""

import sys
from pathlib import Path

from api_bots import printe
from fix_sets.bots.ddo_bot import ddo, studies_fixed_done
from fix_sets.by_count.co import from_files
from fix_sets.by_count.lists import counts_from_files
from fix_sets.new import work_one_study

Dir = Path(__file__).parent


def from_files_get():
    # ---
    da = counts_from_files()
    # ---
    if "from_files" in sys.argv:
        da = from_files()
    # ---
    return da


def doda(ids_by_count, numbs=None):
    # ---
    new = []
    # ---
    sys_ids = [arg.strip() for arg in sys.argv if arg.strip().isdigit()]
    # ---
    if sys_ids or "pp" in sys.argv or numbs:
        by_coun = {}
        # ---
        for study_id, counts in ids_by_count.items():
            if counts not in by_coun:
                by_coun[counts] = []
            by_coun[counts].append(study_id)
        # ---
        by_coun = dict(sorted(by_coun.items(), key=lambda x: x[0], reverse=False))
        # ---
        for counts, ids in by_coun.items():
            if len(ids) > 100 or "pp" in sys.argv:
                printe.output(f"<<purple>> {counts=:,}: {len(ids)=:,}")
            # ---
            to_ge = numbs == counts or str(counts) in sys_ids
            # ---
            if to_ge:
                printe.output(f"<<green>> USE {counts}...")
                new.extend(ids)
    # ---
    if new:
        new = list(set(new))
        new2 = {x: ids_by_count[x] for x in new}
        return new2
    # ---
    return ids_by_count


def remove_done(iui):
    # ---
    print(f"remove_done.  done:{len(studies_fixed_done):,}\t ids:{len(iui):,}")
    # ---
    iui_no_done = {x: v for x, v in iui.items() if x not in studies_fixed_done}
    # ---
    printe.output(f"\t remove_done:\t ids:{len(iui):,} after_done: <<yellow>>{len(iui_no_done):,}")
    # ---
    return iui_no_done


def get_ids_o(numbs=None):
    # ---
    iui = from_files_get()
    # ---
    iui = remove_done(iui)
    # ---
    iui = doda(iui, numbs=numbs)
    # ---
    ids = ddo(list(iui.keys()), spli=False)
    # ---
    ids.sort()
    # ---
    if "reverse" in sys.argv:
        ids.reverse()
    # ---
    ids_by_count = {x: iui[x] for x in ids}
    # ---
    printe.output(f"<<purple>> len of ids: {len(ids_by_count)}")
    printe.output(f"<<purple>> len of ids: {len(ids_by_count)}")
    printe.output(f"<<purple>> len of ids: {len(ids_by_count)}")
    # ---
    ids_by_count2 = dict(sorted(ids_by_count.items(), key=lambda x: x[1], reverse=False))
    # ---
    return ids_by_count2


def main():
    # ---
    ids_by_count2 = get_ids_o()
    # ---
    for n, (study_id, counts) in enumerate(ids_by_count2.items()):
        print(f"_____________\n {n=}/{len(ids_by_count2)}: {counts=}")
        work_one_study(study_id)


if __name__ == "__main__":
    main()
