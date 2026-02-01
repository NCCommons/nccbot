"""


"""
# ---
import functools
import os
import configparser
from newapi import ALL_APIS


@functools.lru_cache(maxsize=1)
def _load_credentials() -> tuple[str, str]:
    home_dir = os.getenv("HOME")
    project = home_dir if home_dir else "I:/ncc"

    config = configparser.ConfigParser()
    config.read(f"{project}/confs/nccommons_user.ini")

    username = config["DEFAULT"].get("username", "").strip()
    password = config["DEFAULT"].get("password", "").strip()

    return username, password


@functools.lru_cache(maxsize=1)
def load_main_api() -> ALL_APIS:
    username, password = _load_credentials()
    return ALL_APIS(lang='www', family='nccommons', username=username, password=password)
