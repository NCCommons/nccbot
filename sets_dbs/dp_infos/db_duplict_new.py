"""
python3 core8/pwb.py fix_db/dp_infos/db_duplict_new test3 fs_infos_duplict-old.sqlite
python3 core8/pwb.py fix_db/dp_infos/db_duplict_new test3
python3 core8/pwb.py fix_db/dp_infos/db_duplict_new 54575469

from sets_dbs.dp_infos.db_duplict_new import insert_url_file # insert_url_file(url, file)

"""

import re
import sys

from sets_dbs.main_db import DbClass


def fix_data(data):
    if data["url"].startswith("/"):
        data["url"] = f"https://prod-images-static.radiopaedia.org/images{data['url']}"

    urlid = data.get("urlid")

    if not urlid and data["url"]:
        # match https://prod-images-static.radiopaedia.org/images/(\d+)/
        ma = re.match(r"https://prod-images-static.radiopaedia.org/images/(\d+)/", data["url"])
        if ma:
            urlid = ma.group(1)

    return {
        "url": data["url"],
        "urlid": urlid,
        "file": data["file"],
    }


class MyDb(DbClass):
    def __init__(self):
        # ---
        self.table_name = "infos"
        self.create_table_query = """
            CREATE TABLE IF NOT EXISTS `infos` (
                `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
                `url` text DEFAULT NULL,
                `urlid` text DEFAULT NULL,
                `file` text DEFAULT NULL
            );
            """
        # ---
        super().__init__(self.table_name, self.create_table_query)
        # ---
        # self.execute(query, params=None)
        # self.executemany(query, params=None)
        # self.get_all()
        # self.do_query(query, values=None, get_data=False)


uu_db = MyDb()


def insert_infos(data):
    """Insert information into the database."""
    data = fix_data(data)
    # ---
    query = "INSERT INTO infos (url, urlid, file) VALUES (%s, %s, %s);"
    values = [data["url"], data["urlid"], data["file"]]
    # ---
    return uu_db.execute(query, params=values)


def insert_url_file(url, file):
    return insert_infos({"url": url, "urlid": "", "file": file})


def insert_all_infos(data_list_or, prnt=True):
    # return main_db_bot.insert_all_infos(data_list_or, prnt=prnt)
    for data in data_list_or:
        insert_infos(data)


def find_data(url="", urlid=""):
    query = "SELECT * from infos WHERE"
    # ---
    if "nodb" in sys.argv:
        return ""
    # ---
    if not url and not urlid:
        return ""
    # ---
    values = []
    _or_ = " or " if url and urlid else ""
    # ---
    if url:
        query += " url = %s"
        values.append(url)
    # ---
    if urlid:
        query += f"{_or_} urlid = %s"
        values.append(urlid)
    # ---
    result = uu_db.do_query(query, values=values, get_data=True)
    # ---
    if result:
        for x in result:
            if x.get("file"):
                return x["file"]
    # ---
    return ""
