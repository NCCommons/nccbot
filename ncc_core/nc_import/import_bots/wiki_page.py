"""
from .wiki_page import load_main_api
main_api = load_main_api("en", "wikipedia")

"""
import os
import functools
import configparser
from newapi import ALL_APIS


@functools.lru_cache(maxsize=1)
def _load_credentials() -> tuple[str, str]:
    home_dir = os.getenv("HOME")
    project = home_dir if home_dir else "I:/ncc"

    config = configparser.ConfigParser()
    config.read(f"{project}/confs/user.ini")

    bot_username = config["DEFAULT"].get("botusername", "").strip()
    bot_password = config["DEFAULT"].get("botpassword", "").strip()
    return bot_username, bot_password


@functools.lru_cache(maxsize=1)
def load_main_api(lang, family="wikipedia") -> ALL_APIS:
    bot_username, bot_password = _load_credentials()
    return ALL_APIS(
        lang=lang,
        family=family,
        username=bot_username,
        password=bot_password,
    )
