"""
from api_bots.wiki_page import load_main_api
main_api = load_main_api("en", "wikipedia")

wiki_NEW_API = NewApi = main_api.NewApi
wiki_MainPage = MainPage = main_api.MainPage
wiki_CatDepth = CatDepth = main_api.CatDepth

"""

import functools

from api_bots import user_account_new
from newapi import AllAPIS

User_tables = {"username": user_account_new.bot_username, "password": user_account_new.bot_password}


@functools.lru_cache(maxsize=1)
def load_main_api(lang, family="wikipedia") -> AllAPIS:
    return AllAPIS(
        lang=lang,
        family=family,
        username=user_account_new.bot_username,
        password=user_account_new.bot_password,
    )
