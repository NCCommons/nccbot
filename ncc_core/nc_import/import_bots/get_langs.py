"""
this bot get langs from nccommons page:
https://nccommons.org/wiki/User:Mr._Ibrahem/import_bot

"""
# import re
import wikitextparser as wtp
from .page_ncc import load_main_api
import logging
logger = logging.getLogger(__name__)


def get_text():
    """
    Retrieves text content from a specific page.
    """
    title = "User:Mr. Ibrahem/import bot"
    main_api = load_main_api()
    page = main_api.MainPage(title)
    text = page.get_text()
    # match all langs like: * ar\n* fr

    return text


def get_langs_codes():
    """
    Extracts language codes from the text content of a page.
    """
    text = get_text()
    langs = []
    # * {{User:Mr. Ibrahem/import bot/line|ar}}

    tmp = "User:Mr. Ibrahem/import bot/line"

    prased = wtp.parse(text)
    temps = prased.templates
    for temp in temps:

        name = str(temp.normal_name()).strip().lower().replace("_", " ")

        logger.info(f"{temp.name=}, {name=}")

        if name == tmp.lower():

            # get first argument

            va = temp.get_arg("1")
            if va and va.value:
                langs.append(va.value.strip())

    logger.info(f"langs: {langs}")

    return langs


if __name__ == "__main__":
    # python3 core8/pwb.py nc_import/bots/get_langs
    get_langs_codes()
