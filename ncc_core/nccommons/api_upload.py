#!/usr/bin/python3
"""

Usage:
from nccommons import api_upload

def upload_by_url():
    return api_upload.upload_by_url(file_name, text, url, comment='')
# ---
"""
import sys
import urllib.request

from api_bots.page_ncc import NEW_API
from nccommons import fix_svg

# ---
from nccommons.ext import get_new_ext
import logging
logger = logging.getLogger(__name__)

api_new = NEW_API()
yes_answer = ["y", "a", "", "Y", "A", "all"]
upload_all = {1: False}

def download_file(url):
    """
    Downloads a file from a given URL to a temporary location.
    """
    try:
        # Download the file to a temporary location
        temp_file_path, _ = urllib.request.urlretrieve(url)
        print(f"File downloaded to: {temp_file_path}")
        return temp_file_path
    except Exception as e:
        print(f"An error occurred while downloading the file: {e}")
        return None

def do_post(params, code="", family="", files=None):
    """
    Makes a POST request to the Wikipedia API with specified parameters.
    """
    # ---
    params["format"] = "json"
    params["utf8"] = 1
    # ---
    # api_new.Login_to_wiki()
    # ---
    result = api_new.post_params(params, addtoken=True, files=files)
    # ---
    return result

def upload_by_file(file_name, text, url, comment="", code="en", family="wikipedia", fix_svg_dtd=False):
    """
    Uploads a file to Wikipedia using a local file.
    """
    # ---
    if file_name.startswith("File:"):
        file_name = file_name.replace("File:", "")
    # ---
    # get the file from url
    file_path = download_file(url)
    # ---
    if not file_path:
        logger.info(f"<<lightred>> download file failed, {url=}")
        return False
    # ---
    logger.info(f"<<lightyellow>> {file_path=}...")
    # ---
    if file_name.endswith(".svg") and fix_svg_dtd:
        file_path = fix_svg.remove_svg_dtd(file_path)
    # ---
    params = {
        "action": "upload",
        "format": "json",
        "filename": file_name,
        "comment": comment,
        "text": text,
        "utf8": 1,
    }
    # ---
    # data = do_post(params, code=code, family=family, files={"file": open(file_path, "rb")})
    data = do_post(params, files={"file": open(file_path, "rb")})
    # ---
    upload_result = data.get("upload", {})
    # ---
    # {"upload": {"result": "Warning", "warnings": {"duplicate": ["....jpg"]}}}
    # ---
    success = upload_result.get("result") == "Success"
    error = data.get("error", {})
    # ---
    duplicate = upload_result.get("warnings", {}).get("duplicate", [""])[0].replace("_", " ")
    # ---
    if success:
        logger.info(f"<<lightgreen>> ** upload true .. [[File:{file_name}]] ")
        return True

    if duplicate:
        logger.info(f"<<lightred>> ** duplicate file:  {duplicate}.")

    if error:
        error_code = error.get("code", "")
        error_info = error.get("info", "")
        logger.info(f"<<lightred>> error when upload_by_url, error_code:{error_code}")
        # ---
        # if error_code == "verification-error":
        #     if do_ext and "MIME type of the file" in error_info:
        #         new_file_name = get_new_ext(error_info, "wiki.jpg")
        #         if new_file_name:
        #             return upload_by_file(url, filename=new_file_name, do_ext=False)
        # else:
        logger.info(error)

    # ---
    return False

def do_ask(text, file_name):
    # ---
    if "nodiff" not in sys.argv:
        logger.info(text)
    # ---
    logger.info(f"<<lightyellow>> {__name__}: upload file:'{file_name}' ? ([y]es, [N]o)")
    sa = input()
    # ---
    if sa.strip() not in ["y", "a", "", "Y", "A", "all"]:
        logger.info("<<lightred>> wrong answer")
        return False
    # ---
    if sa.strip() == "a":
        logger.info("---------------------------------------------")
        logger.info(f"{__name__} upload_by_url save all without asking.")
        logger.info("---------------------------------------------")
        upload_all[1] = True
    # ---
    return True

def upload_by_url(
    file_name, text, url, comment="", return_file_name=False, do_ext=False, code="en", family="wikipedia"
):
    """

    Uploads a file to Wikipedia using a URL.

    """
    # ---
    if not url:
        logger.info("<<lightred>>upload_by_url: no url")
        return False
    # ---
    if file_name.startswith("File:"):
        file_name = file_name.replace("File:", "")
    # ---
    params = {
        "action": "upload",
        "format": "json",
        "filename": file_name,
        "url": url,
        "comment": comment,
        "text": text,
        "utf8": 1,
    }
    # ---
    if "ask" in sys.argv and not upload_all[1]:
        ask = do_ask(text, file_name)
        if not ask:
            return file_name
    # ---
    # {'upload': {'result': 'Success', 'filename': 'Pediculosis_Palpebrarum_(Dermatology_Atlas_1).jpg', 'imageinfo': {'timestamp': '2023-11-29T20:12:26Z', 'user': 'Mr. Ibrahem', 'userid': 13, 'size': 52289, 'width': 506, 'height': 379, 'parsedcomment': '', 'comment': '', 'html': '', 'canonicaltitle': 'File:Pediculosis Palpebrarum (Dermatology Atlas 1).jpg', 'url': 'https://nccommons.org/media/f/fd/Pediculosis_Palpebrarum_%28Dermatology_Atlas_1%29.jpg', 'descriptionurl': 'https://nccommons.org/wiki/File:Pediculosis_Palpebrarum_(Dermatology_Atlas_1).jpg', 'sha1': '1df195d80a496c6aadcefbc6d7b8adf13caddafc', 'metadata': [{'name': 'JPEGFileComment', 'value': [{'name': 0, 'value': 'File written by Adobe Photoshop¨ 4.0'}]}, {'name': 'MEDIAWIKI_EXIF_VERSION', 'value': 2}], 'commonmetadata': [{'name': 'JPEGFileComment', 'value': [{'name': 0, 'value': 'File written by Adobe Photoshop¨ 4.0'}]}], 'extmetadata': {'DateTime': {'value': '2023-11-29T20:12:26Z', 'source': 'mediawiki-metadata', 'hidden': ''}, 'ObjectName': {'value': 'Pediculosis Palpebrarum (Dermatology Atlas 1)', 'source': 'mediawiki-metadata', 'hidden': ''}}, 'mime': 'image/jpeg', 'mediatype': 'BITMAP', 'bitdepth': 8}}}
    # ---
    data = do_post(params)
    # ---
    upload_result = data.get("upload", {})
    # ---
    # {"upload": {"result": "Warning", "warnings": {"duplicate": ["....jpg"]}}}
    # ---
    duplicate = upload_result.get("warnings", {}).get("duplicate", [""])[0].replace("_", " ")
    # ---
    success = upload_result.get("result") == "Success"
    error = data.get("error", {})
    # ---
    # { "upload": { "result": "Warning", "warnings": { "exists": "Axillary_hidradenitis_suppurativa_(Radiopaedia_91902-109711_None_2).png", "nochange": { "timestamp": "2024-01-09T02:30:04Z" } }, "filekey": "x.", "sessionkey": "x" } }
    # ---
    # {'upload': {'result': 'Warning', 'warnings': {'duplicate': ['Buckle_fracture_of_distal_radius_(Radiopaedia_46707).jpg']}, 'filekey': '1amgwircbots.rdrfjg.13.', 'sessionkey': '1amgwircbots.rdrfjg.13.'}}
    # ---
    exists = upload_result.get("warnings", {}).get("exists", "").replace("_", " ")
    # ---
    error = data.get("error", {})
    # ---
    du = ""
    # ---
    if success:
        new_filename = upload_result.get("filename") or file_name
        # { "upload": { "result": "Success", "filename": "Test1x.jpeg", "imageinfo": { "timestamp": "2024-07-24T22:28:32Z", "user": "Mr. Ibrahem", "userid": 13, "size": 67938, "width": 512, "height": 512, "parsedcomment": "", "comment": "", "html": "", "canonicaltitle": "File:Test1x.jpeg", "url": "https://nccommons.org/media/3/3f/Test1x.jpeg", "descriptionurl": "", "sha1": "e145b86530458d59bd0d9f3b709954d5301a18c9", "metadata": [ { "name": "MEDIAWIKI_EXIF_VERSION", "value": 2 } ], "commonmetadata": [], "extmetadata": { "DateTime": { "value": "2024-07-24T22:28:32Z", "source": "mediawiki-metadata", "hidden": "" }, "ObjectName": { "value": "Test1x", "source": "mediawiki-metadata" } }, "mime": "image/jpeg", "mediatype": "BITMAP", "bitdepth": 8 } } }
        logger.info(f"<<green>> new upload Success, File:{new_filename}")
        return f"File:{new_filename}"

    elif duplicate:
        du = "File:" + duplicate
        # ---
        logger.info(f"duplicate, find url_file_upload: {du}")
        return du

    elif exists:
        du = "File:" + exists
        du = du.replace("_", " ")
        # ---
        logger.info(f"exists, find url_file_upload: {du}")
        return du

    elif error:
        error_code = error.get("code", "")
        error_info = error.get("info", "")
        # ---
        logger.info("____________________________________________")
        logger.info(f"<<yellow>> {file_name=}, {url=}")
        logger.info(f"<<lightred>> error when upload_by_url, error_code:{error_code}")
        # ---
        logger.info(f"<<lightred>> url: {url}")
        # ---
        logger.info(error)
        # ---
        errors = ["copyuploadbaddomain", "copyuploaddisabled"]
        if error_code in errors or " url " in error_info.lower():
            return upload_by_file(file_name, text, url, comment=comment, code=code, family=family)
        # ---
        if error_code == "verification-error":
            if do_ext and "MIME type of the file" in error_info:
                new_file_name = get_new_ext(error_info, file_name)
                if new_file_name:
                    return upload_by_url(new_file_name, text, url, comment=comment, return_file_name=return_file_name)
            # ---
            # {'error': {'code': 'verification-error', 'info': 'Cannot upload SVG files that contain a non-standard DTD declaration.', 'details': ['upload-scripted-dtd'], '*': ''}}
            # ---
            if error_info == "Cannot upload SVG files that contain a non-standard DTD declaration.":
                return upload_by_file(file_name, text, url, comment=comment, code=code, family=family, fix_svg_dtd=True)
    else:
        print(data)
    # ---
    return du
