"""

python3 core8/pwb.py fix_sets/name_bots/get_rev 20060
python3 core8/pwb.py fix_sets/name_bots/get_rev 132518

from fix_sets.name_bots.get_rev import get_images_ids, get_file_urls_rev # get_file_urls_rev(study_id)

"""

import tqdm
import sys
import re
import json

# from pathlib import Path

from api_bots import printe
from fix_sets.ncc_api import post_ncc_params

# from fix_mass.files import study_to_case_cats
from fix_sets.bots.study_files import get_study_files
from fix_sets.jsons_dirs import get_study_dir
from fix_mass.helps_bot.file_bot import from_cach, dumpit
from fix_sets.bots2.match_helps import match_id  # match_id(content, title)

images_to_ids = {}
ids_to_images = {}


# studies_rev_dir = jsons_dir / "studies_rev"


def dump_st(data, study_id):
    # ---
    # file = studies_rev_dir / f"{study_id}.json"
    # ---
    study_id_dir = get_study_dir(study_id)
    # ---
    file = study_id_dir / "rev.json"
    # ---
    dumpit(data, file)


def get_cach_one_study(study_id):
    # ---
    if "nocach" in sys.argv:
        return {}
    # ---
    study_id_dir = get_study_dir(study_id)
    # ---
    file = study_id_dir / "rev.json"
    # ---
    return from_cach(file)


def match_img_url_from_content(content):
    # find urls
    urls = re.findall(r"(?P<url>https?://[^\s]+)", content)
    # ---
    for url in urls:
        if "prod-images-static.radiopaedia.org" in url:
            return url
    # ---
    return ""


def get_images_ids(title="", img_id=""):
    if "noid" in sys.argv:
        return ""

    if title:
        return images_to_ids.get(title)
    elif img_id:
        return ids_to_images.get(img_id)

    return ""


def get_file_rev(title):
    # ---
    params = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "titles": title,
        "utf8": 1,
        "formatversion": "2",
        "rvprop": "content",
        "rvslots": "main",
        "rvlimit": "10",
        "rvdir": "newer",
    }
    data = post_ncc_params(params)
    # ---
    error = data.get("error", {})
    if error:
        printe.output(json.dumps(error, indent=2))
    # ---
    pages = data.get("query", {}).get("pages", [])
    # ---
    img_id = ""
    urlx = ""
    # ---
    for page in pages:
        title = page.get("title")
        # ---
        revisions = page.get("revisions")
        # ---
        if not revisions:
            continue
        # ---
        for x in revisions:
            content = x["slots"]["main"]["content"]
            # ---
            if not img_id:
                img_id = match_id(content, title)
            # ---
            if not urlx:
                url = match_img_url_from_content(content)
                # ---
                if url:
                    urlx = url
            # ---
            if img_id and urlx:
                break
    # ---
    if img_id:
        images_to_ids[title] = img_id
        ids_to_images[img_id] = title
    # ---
    data = {"url": urlx, "id": img_id}
    # ---
    return data


def get_rev_infos(files):
    # ---
    if "norevip" in sys.argv:
        return {}
    # ---
    printe.output(f"get_rev_infos: {len(files)=}")
    # ---
    info = {}
    # ---
    for file in tqdm.tqdm(files):
        info[file] = get_file_rev(file)
    # ---
    return info


def get_file_urls_rev(study_id, files=None, only_cach=False):
    na = {}
    # ---
    if not files:
        files = get_study_files(study_id)
    # ---
    cach = get_cach_one_study(study_id)
    # ---
    files2 = []
    # ---
    if cach:
        files2 = [x for x in files if not cach.get(x) or not (cach.get(x, {}).get("url") and cach.get(x, {}).get("id"))]
        # ---
        if files2:
            printe.output(f"get_file_urls_rev: files2: {len(files2)=}")
    else:
        print(f"no rev cach for: {study_id}")
    # ---
    if (cach or only_cach) and not files2:
        return cach
    # ---
    if not files:
        printe.output(f"Files not found for: {study_id}")
        return na
    # ---
    if files2:
        files = files2
    # ---
    na = get_rev_infos(files)
    # ---
    if not na:
        return {}
    # ---
    if na == cach:
        return na
    # ---
    if cach:
        cach.update(na)
        # ---
        dump_st(cach, study_id)
    else:
        dump_st(na, study_id)
    # ---
    return na


if __name__ == "__main__":
    ids = [arg.strip() for arg in sys.argv if arg.strip().isdigit()]
    # ---
    for x in ids:
        ii = get_file_urls_rev(x)
        # ---
        printe.output(json.dumps(ii, indent=2))
    # ---
    filett = [
        "File:Angiodysplasia - cecal active bleed (Radiopaedia 168775-136954 Coronal 91).jpeg",
        "File:'Bovine' aortic arch (Radiopaedia 33554-34637 Axial lung window 19).png",
        "File:Diffuse uterine adenomyosis (Radiopaedia 156164-128503 Sagittal 23).jpg",
        "File:Angiodysplasia - cecal active bleed (Radiopaedia 168775-136954 Coronal 90).jpeg",
    ]
    # ---
    for x in filett:
        print("------------")
        print(x)
        result = get_file_rev(x)
        print(f"{result=}")
