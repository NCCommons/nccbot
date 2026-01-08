"""

from api_bots.ncc_page import ncc_MainPage, ncc_NEW_API

"""
# ---
import functools
import os
import configparser
from newapi import ALL_APIS

home_dir = os.getenv("HOME")
project = home_dir if home_dir else "I:/ncc"
# ---
config = configparser.ConfigParser()
config.read(f"{project}/confs/nccommons_user.ini")
# ---
username = config["DEFAULT"].get("username", "").strip()
password = config["DEFAULT"].get("password", "").strip()


@functools.lru_cache(maxsize=1)
def load_main_api() -> ALL_APIS[str, str, str, str]:
    return ALL_APIS(lang='www', family='nccommons', username=username, password=password)


main_api = load_main_api()

ncc_NEW_API = main_api.NEW_API
ncc_MainPage = main_api.MainPage

NEW_API = main_api.NEW_API
MainPage = main_api.MainPage
CatDepth = main_api.CatDepth
