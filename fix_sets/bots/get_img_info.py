"""

python3 core8/pwb.py fix_sets/bots/get_img_info

from fix_sets.bots.get_img_info import one_img_info

"""

import json
import re
import sys

# import os
from api_bots import printe
from fix_mass.helps_bot.file_bot import dumpit, from_cach
from fix_sets.bots2.match_helps import match_id, match_urlid
from fix_sets.jsons_dirs import get_study_dir  # , jsons_dir
from fix_sets.ncc_api import post_ncc_params

# st_dic_infos = jsons_dir / "studies_files_infos"


def dump_st(data, study_id):
    # ---
    study_id_dir = get_study_dir(study_id)
    # ---
    file = study_id_dir / "img_info.json"
    # ---
    dumpit(data, file)


def get_cach_img_info(study_id):
    # ---
    study_id_dir = get_study_dir(study_id)
    # ---
    file = study_id_dir / "img_info.json"
    # ---
    return from_cach(file)


def match_them(extlinks, revisions, title, id_to_url):
    data = {"img_url": "", "img_id": ""}
    # ---
    ma_id = ""
    # ---
    if revisions:
        revisions = revisions[0]["content"]
        ma_id = match_id(revisions, title)
    # ---
    if ma_id:
        data["img_id"] = ma_id
        data["img_url"] = id_to_url.get(str(ma_id), "")
    else:
        print(revisions)
        # ---
        for extlink in extlinks:
            url = extlink.get("url")
            if url.find("radiopaedia.org/images/") != -1:
                data["img_url"] = url
                data["img_id"] = match_urlid(url)
                break
    # ---
    return data


def gt_img_info(titles, id_to_url=None):
    # ---
    if not id_to_url:
        id_to_url = {}
    # ---
    # titles = [x for x in titles if x]
    # ---
    info = {}
    printe.output(f"one_img_info: {len(titles)=}")
    # ---
    params = {
        "action": "query",
        # "titles": "|".join(titles),
        # "prop": "revisions|categories|info|extlinks",
        "prop": "revisions|extlinks",
        # "clprop": "sortkey|hidden", # categories
        "rvprop": "content",  # revisions
        # "cllimit": "max",  # categories
        "ellimit": "max",  # extlinks
        "formatversion": "2",
    }
    # ---
    # work with 40 titles at once
    for i in range(0, len(titles), 40):
        group = titles[i : i + 40]
        params["titles"] = "|".join(group)
        # ---
        # print("|".join(group))
        # ---
        data = post_ncc_params(params)
        # ---
        error = data.get("error", {})
        if error:
            printe.output(json.dumps(error, indent=2))
        # ---
        pages = data.get("query", {}).get("pages", [])
        # ---
        for page in pages:
            extlinks = page.get("extlinks", [])
            revisions = page.get("revisions")
            title = page.get("title")
            # ---
            info[title] = match_them(extlinks, revisions, title, id_to_url)
    # ---
    printe.output(json.dumps(info, indent=2))
    # ---
    return info


def one_img_info(files, study_id, json_data):
    # ---
    if "oo" not in sys.argv:
        return {}
    # ---
    cach = get_cach_img_info(study_id)
    if cach:
        return cach
    # ---
    id_to_url = {}
    # ---
    for x in json_data:
        for image in x["images"]:
            id_to_url[str(image["id"])] = image["public_filename"]
    # ---
    info = gt_img_info(files, id_to_url)
    # ---
    dump_st(info, study_id)
    # ---
    return info


def test():
    title = [
        "File:1st metatarsal head fracture (Radiopaedia 99187-120594 Frontal 1).png",
        "File:Appendicitis (CT angiogram) (Radiopaedia 154713-134732 This comic explains the pathophysiology of appendicitis. 02).jpg",
    ]
    info = gt_img_info(title)
    # ---
    print(json.dumps(info, indent=2))


if __name__ == "__main__":
    test()
