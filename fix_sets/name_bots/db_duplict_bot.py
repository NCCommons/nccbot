"""

from fix_sets.name_bots.db_duplict_bot import find_url_file_upload

python3 core8/pwb.py fix_sets/name_bots/db_duplict_bot

"""

import re
import sys

from api_bots import printe
from fix_sets.name_bots.upload_to_api import get_from_api
from sets_dbs.dp_infos.db_duplict_new import (  # ,find_from_data_db as find_from_db_dp # insert_url_file(url, file)
    find_data,
    insert_all_infos,
    insert_url_file,
)

data_maain = {}

# db_data = get_all_key_url_urlid()
db_data = {}


def insert_infos_all(data):
    try:
        return insert_all_infos(data)
    except Exception as e:
        printe.output(f"<<red>> Error insert_all_infos: {str(e)}")


def match_urlid(url):
    # ---
    url_id = ""
    # ---
    # find id from url like: https://prod-images-static.radiopaedia.org/images/(\d+)/.*?$
    mat = re.match(r"https://prod-images-static.radiopaedia.org/images/(\d+)/.*?$", url)
    if mat:
        url_id = mat.group(1)
    # ---
    return url_id


def append_data(url, file_name):
    data_maain[url] = file_name
    # ---
    result = insert_url_file(url, file_name)
    # ---
    printe.output(f"<<green>> append_data: {url} -> {file_name} -> {result}")


def from_cach_or_db(url, url_id=""):
    # ---
    if url in data_maain:
        da = data_maain[url]
        if da.find("https") == -1:
            # printe.output(f"find url_file_upload: {data_maain[url]}")
            return da
    # ---
    # file_name = find_from_db_dp(url, "")
    file_name = ""
    # ---
    # file_name = db_data.get(url) or (db_data.get(url_id) if url_id else "")
    # ---
    file_name = find_data(url=url, urlid=url_id)
    # ---
    if file_name:
        printe.output(f"<<green>> find_from_data_db: {url} -> {file_name}")
    # ---
    return file_name


def find_url_file_upload(url, file_name_to_upload, do_api, file_text, noapi=False):
    # ---
    url_id = match_urlid(url)
    # ---
    in_cach = from_cach_or_db(url, url_id)
    # ---
    if in_cach and in_cach.find("https") == -1:
        # printe.output(f"find url_file_upload, from_cach_or_db: {in_cach}")
        return in_cach
    # ---
    na = ""
    # ---
    if "noapi" not in sys.argv:
        if do_api and not noapi:
            na = get_from_api(url, filename=file_name_to_upload, file_text=file_text)
    # ---
    if na:
        na = na.replace("_", " ")
        append_data(url, na)
    # ---
    return na


if __name__ == "__main__":
    # ---
    url = "https://prod-images-static.radiopaedia.org/images/41297969/ebc7b3d1e1f61485f3aa37071c66f8.png"
    # ---
    print(f"{url=}")
    # ---
    print(from_cach_or_db(url))
    # ---
    url_id = "1159649"
    # ---
    print(f"{url_id=}")
    # ---
    print(from_cach_or_db("", url_id=url_id))
