"""

python3 core8/pwb.py mass/st3/miss

tfj run miss --image python3.9 --command "$HOME/local/bin/python3 c8/pwb.py mass/st3/miss"

"""

import json
import sys

from mass.radio.jsons_bot import radio_jsons_dir
from mass.st3.start import main

with open(radio_jsons_dir / "all_ids.json", encoding="utf-8") as f:
    all_ids = json.load(f)

lista = """
    182746
    176190
    """
# ---
new_ids = [x.strip() for x in lista.split("\n") if x.strip()]
# ---
# Parsing arguments
lookup_dict = {x: (all_ids.get(x) or all_ids.get(int(x))) for x in new_ids if x in all_ids}

print(f"len new_ids: {len(new_ids)}")
print(f"len lookup_dict: {len(lookup_dict)}")
# ---
if "start" in sys.argv:
    main(lookup_dict)
