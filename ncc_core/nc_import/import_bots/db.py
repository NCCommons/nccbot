"""

"""
# ---

import os
import jsonlines
from .db_bot import LiteDB

root_path = "I:" if os.path.exists("I:") else "/data/project/"

db_path = f"{root_path}/ncc/public_html/ncc2/lists/nc_files.db"
jsonl_path = f"{root_path}/ncc/public_html/ncc2/lists/nc_files.jsonl"


def add_to_txt(data):
    if not os.path.exists(jsonl_path):
        with open(jsonl_path, "w", encoding="utf-8") as f:
            f.write("")
    # ---
    # with open(jsonl_path, "a", encoding="utf-8") as f:
    #     f.write(f"{json.dumps(data, ensure_ascii=False)}\n")
    # ---
    with jsonlines.open(jsonl_path, mode="a") as writer:
        writer.write(data)


def add_to_jsonl(data):
    if not os.path.exists(jsonl_path):
        with open(jsonl_path, "w", encoding="utf-8") as f:
            f.write("")
    with jsonlines.open(jsonl_path, mode="a") as writer:
        writer.write(data)


def create():
    nc_files_db = LiteDB(db_path)
    nc_files_db.create_table(
        "nc_files",
        {"id": int, "lang": str, "title": str, "views": int, "dat": str},
        pk="id",
        defaults={"views": 0},
    )


def add_to_db(title, code):
    nc_files_db = LiteDB(db_path)
    data = {"lang": code, "title": title}

    nc_files_db.insert("nc_files", data)

    # append data to file
    add_to_jsonl(data)


if __name__ == "__main__":
    nc_files_db = LiteDB(db_path)
    create()

    add_to_db('File:Chondrosarcoma_of_the_nasal_septum_(Radiopaedia_165701-135935_Sagittal_2)".jpeg', "af")

    data = nc_files_db.get_data("nc_files")
    for row in data:
        print(row)
