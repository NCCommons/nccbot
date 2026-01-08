"""

python3 core8/pwb.py nc_import/bot ask

"""
import sys
from bots.wrk_pages import work_on_pages
from bots.get_langs import get_langs_codes
from api_bots.wiki_page import load_main_api


def get_pages(code):
    """
    Retrieves template pages related to a given language code.
    """
    main_api = load_main_api(code, "wikipedia")
    api_new = main_api.NEW_API()

    api_new.Login_to_wiki()

    pages = api_new.Get_template_pages("Template:NC", namespace="*", Max=10000)

    return pages


def start():
    """
    A function that starts the process by iterating over languages, getting pages for each language, and then working on those pages.
    """
    lang = ""
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(":")
        if arg == "-lang":
            lang = value
    # ---
    langs = get_langs_codes()
    # ---
    if lang and lang in langs:
        langs = [lang]
    # ---
    for code in langs:
        pages = get_pages(code)
        work_on_pages(code, pages)


if __name__ == "__main__":
    start()
