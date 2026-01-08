"""

from fix_sets.by_count.lists import counts_from_files


"""
import json
from pathlib import Path

from api_bots import printe

Dir = Path(__file__).parent


def counts_from_files():
    # ---
    files_file = Dir / "by_count.json"
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
    return lisst_of_s
