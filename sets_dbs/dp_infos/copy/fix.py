""" """

import os
from pathlib import Path

from tqdm import tqdm

home_dir = os.getenv("HOME")
project = home_dir if home_dir else "I:/ncc"
Dir = Path(project) / "ncc_data/sets_dbs/dp_infos/copy"

files = {
    "new": "new.sql",
    "errors": "errors.sql",
}

for k, v in files.items():
    file = Dir / v
    if not file.exists():
        print(f"File not found: {file}")
        file.touch()


def addtofile(file, line):
    file_path = Dir / file
    with open(file_path, "a") as f:
        f.write(line)
        f.write("\n")


errors = 0
done = 0

sqlpath = Dir / "adminer.sql"

with open(sqlpath, "r") as f:
    # ---
    for line in tqdm(f, total=7083106):
        line = line.strip()
        if line.endswith(";") and line.startswith("INSERT INTO infos"):
            if line.count("'") == 6:
                done += 1
                addtofile("new.sql", line)
            elif line.count("'") > 6:
                line = line.replace("('", '("').replace("')", '")').replace("', '", '", "')
                done += 1
                addtofile("new.sql", line)
            else:
                errors += 1
                addtofile("errors.sql", line)

print("Data inserted successfully!")
print(f"Total errors: {errors}")
print(f"Total rows inserted: {done}")
