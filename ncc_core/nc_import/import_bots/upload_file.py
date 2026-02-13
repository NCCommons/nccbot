#!/usr/bin/python3
"""


"""
import urllib.request
from .wiki_page import load_main_api

import logging
logger = logging.getLogger(__name__)


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


def do_post(code, family, params, files=None):
    """
    Makes a POST request to the Wikipedia API with specified parameters.
    """
    main_api = load_main_api(code, family)
    api_new = main_api.NEW_API()

    if files:
        result = api_new.post_params(params, addtoken=True, files=files)
    else:
        result = api_new.post_params(params, addtoken=True)

    return result


def upload_by_file(file_name, text, url, comment="", code="en", family="wikipedia"):
    """
    Uploads a file to Wikipedia using a local file.
    """

    if file_name.startswith("File:"):
        file_name = file_name.replace("File:", "")

    file_path = download_file(url)

    params = {"action": "upload", "format": "json", "filename": file_name, "comment": comment, "text": text, "utf8": 1}

    result = do_post(code, family, params, files={"file": open(file_path, "rb")})

    upload_result = result.get("upload", {})

    success = upload_result.get("result") == "Success"
    error = result.get("error", {})
    error_code = result.get("error", {}).get("code", "")

    duplicate = upload_result.get("warnings", {}).get("duplicate", [""])[0].replace("_", " ")

    if success:
        logger.info(f"<<lightgreen>> ** upload true .. [[File:{file_name}]] ")
        return True

    if duplicate:
        logger.info(f"<<lightred>> ** duplicate file:  {duplicate}.")

    if error:
        logger.info(f"<<lightred>> error when upload_by_file, error_code:{error_code}")
        logger.info(error)

    return False


def upload_by_url(file_name, text, url, comment="", code="en", family="wikipedia"):
    """
    Uploads a file to Wikipedia using a URL.
    """

    if file_name.startswith("File:"):
        file_name = file_name.replace("File:", "")

    params = {"action": "upload", "format": "json", "filename": file_name, "url": url, "comment": comment, "text": text, "utf8": 1}

    result = do_post(code, family, params)

    upload_result = result.get("upload", {})

    success = upload_result.get("result") == "Success"
    error = result.get("error", {})
    error_code = result.get("error", {}).get("code", "")
    error_info = result.get("error", {}).get("info", "")

    # {'upload': {'result': 'Warning', 'warnings': {'duplicate': ['Buckle_fracture_of_distal_radius_(Radiopaedia_46707).jpg']}, 'filekey': '1amgwircbots.rdrfjg.13.', 'sessionkey': '1amgwircbots.rdrfjg.13.'}}

    duplicate = upload_result.get("warnings", {}).get("duplicate", [""])[0].replace("_", " ")

    if success:
        logger.info(f"<<lightgreen>> ** true .. [[File:{file_name}]] ")
        return True

    if duplicate:
        logger.info(f"<<lightred>> ** duplicate file:  {duplicate}.")

    if error:
        logger.info(f"<<lightred>> error when upload_by_url, error_code:{error_code}")
        logger.info(error_info)
    errors = ["copyuploadbaddomain", "copyuploaddisabled"]
    if error_code in errors or " url " in error_info.lower():
        return upload_by_file(file_name, text, url, comment=comment, code=code, family=family)

    return False
