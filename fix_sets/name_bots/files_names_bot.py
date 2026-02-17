"""

from fix_sets.name_bots.files_names_bot import get_files_names

"""

import re
import sys

# import json
import tqdm

# from sets_dbs.file_infos.db import get_all_key_url_urlid  # , find_from_data_db  # find_from_data_db(url, urlid)
from fix_mass.helps_bot.file_bot import dumpit, from_cach
from fix_sets.bots.study_files import get_study_files

# from fix_sets.lists.sf_infos import from_sf_infs  # from_sf_infs(url, study_id)
from fix_sets.jsons_dirs import get_study_dir
from fix_sets.name_bots.db_duplict_bot import find_url_file_upload, insert_infos_all
from fix_sets.name_bots.get_rev import get_file_urls_rev  # get_file_urls_rev(study_id)
import logging
logger = logging.getLogger(__name__)

# db_data = get_all_key_url_urlid()
db_data = {}

# studies_names_dir = jsons_dir / "studies_names"
data_uu = {}

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

def dump_it(data2, cach, study_id):
    # ---
    # file = studies_names_dir / f"{study_id}.json"
    # ---
    data2 = {x: v for x, v in data2.items() if v}
    # ---
    if data2 == cach:
        return
    # ---
    study_id_dir = get_study_dir(study_id)
    # ---
    file = study_id_dir / "names.json"
    # ---
    if not cach:
        dumpit(data2, file)
        return
    # ---
    data = cach.copy()
    # ---
    for x in data2:
        if not data.get(x):
            data[x] = data2[x]
    # ---
    dumpit(data, file)
    # ---
    new_data = [{"url": url, "urlid": "", "file": file} for url, file in data.items()]
    # ---
    insert_infos_all(new_data)

def get_names_from_cach(study_id):
    # ---
    study_id_dir = get_study_dir(study_id)
    # ---
    file = study_id_dir / "names.json"
    # ---
    cca = from_cach(file)
    # ---
    if cca:
        cca = {x: v for x, v in cca.items() if v}
    # ---
    return cca

def get_file_name_dd(url, study_id, url_id):
    # ---
    data_uu.setdefault(study_id, {})
    # ---
    if url in data_uu.get(study_id, {}):
        return data_uu[study_id][url]
    # ---
    file_name = ""
    # ---
    if not file_name:
        # file_name = find_from_data_db(url, url_id)
        file_name = db_data.get(url) or (db_data.get(url_id) if url_id else "")
        # ---
        # if file_name: logger.info(f"<<1green>> find_from_data_db: {url} -> {file_name}")
    # # ---
    # if not file_name:
    #     do_api = "noapi" not in sys.argv
    #     file_name = find_url_file_upload(url, "", do_api)
    # ---
    data_uu[study_id][url] = file_name
    # ---
    return file_name

def get_file_name_no_dd(url, url_to_file):
    file_name = ""
    # ---
    if not file_name:
        if "oo" in sys.argv:
            file_name = url_to_file.get(url)
    # ---
    # if not file_name: file_name = from_sf_infs(url, study_id)
    # ---
    return file_name

def get_file_name_rev(url, url_data_to_file, rev_id_to_file):
    # ---
    url_id = match_urlid(url)
    # ---
    file_name = ""
    # ---
    if not file_name:
        file_name = url_data_to_file.get(url, "")
    # ---
    if not file_name and url_id:
        file_name = rev_id_to_file.get(url_id, "")
    # ---
    return file_name

def make_names_2(urls, study_id, files, study_infos={}, noapi=False):
    logger.info(f"no_names: {len(urls)}")
    # ---
    only_cach = "revcach" in sys.argv
    # ---
    url_data2 = get_file_urls_rev(study_id, files=files, only_cach=only_cach)
    # ---
    url_data_to_file = {d["url"]: file for file, d in url_data2.items() if d.get("url")}
    # ---
    rev_id_to_file = {d["id"]: file for file, d in url_data2.items() if d.get("id")}
    # ---
    names2 = {}
    # ---
    for url in tqdm.tqdm(urls):
        # ---
        file_name_to_upload = study_infos.get(url, {}).get("file", "")
        file_text = study_infos.get(url, {}).get("text", "")
        # ---
        file_name = get_file_name_rev(url, url_data_to_file, rev_id_to_file)
        # ---
        if not file_name and "new2" in sys.argv:
            file_name = file_name_to_upload
        # ---
        if not file_name:
            do_api = "noapi" not in sys.argv
            file_name = find_url_file_upload(url, file_name_to_upload, do_api, file_text, noapi=noapi)
        # ---
        if file_name:
            names2[url] = file_name
    # ---
    data_uu[study_id].update(names2)
    # ---
    return names2

def get_files_names(urls, url_to_file, study_id, files=None, study_infos={}, noapi=False):
    # ---
    if not files:
        files = get_study_files(study_id)
    # ---
    if study_id not in data_uu:
        data_uu[study_id] = {}
    # ---
    cach = get_names_from_cach(study_id)
    # ---
    files_names = {}
    # ---
    for url in urls:
        # ---
        # logger.info(f"<<yellow>> get_files_names: {n}/{len(urls)}: {url}")
        # ---
        url_id = match_urlid(url)
        # ---
        file_name = cach.get(url)
        # ---
        if not file_name:
            file_name = get_file_name_dd(url, study_id, url_id)
        # ---
        if not file_name:
            file_name = get_file_name_no_dd(url, url_to_file)
        # ---
        if file_name and not file_name.startswith("File:"):
            file_name = "File:" + file_name
        # ---
        files_names[url] = file_name
    # ---
    no_names = [x for x in urls if not files_names.get(x)]
    # ---
    if no_names:
        names_2 = make_names_2(no_names, study_id, files, study_infos=study_infos, noapi=noapi)
        if names_2:
            files_names.update(names_2)
    # ---
    if data_uu[study_id]:
        dump_it(data_uu[study_id], cach, study_id)
    # ---
    return files_names
