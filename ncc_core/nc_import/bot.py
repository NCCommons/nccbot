"""

python3 core8/pwb.py nc_import/bot ask

"""
import sys
from import_bots.wrk_pages import work_on_pages
from import_bots.get_langs import get_langs_codes
from import_bots.wiki_page import load_main_api


def Get_template_pages(code, title, namespace="*", Max=10000):
    # ---
    main_api = load_main_api(code, "wikipedia")
    api_new = main_api.NEW_API()
    # ---
    print(f'Get_template_pages for template:"{title}", limit:"{Max}",namespace:"{namespace}"')
    # ---
    params = {
        "action": "query",
        "titles": title,
        "generator": "transcludedin",
        "gtinamespace": namespace,
        "gtilimit": "max",
        "formatversion": "2",
    }
    # ---
    results = api_new.post_continue(params, "query", _p_="pages", p_empty=[])
    # ---
    pages = [x["title"] for x in results]
    # ---
    print(f"mdwiki_api.py Get_template_pages : find {len(pages)} pages.")
    # ---
    return pages


def get_pages(code):
    """
    Retrieves template pages related to a given language code.
    """
    pages = Get_template_pages(code, "Template:NC", namespace="*", Max=10000)

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
