"""


"""
import functools
from newapi import ALL_APIS

from api_bots import user_account_new
User_tables = {"username": user_account_new.bot_username, "password": user_account_new.bot_password}


@functools.lru_cache(maxsize=1)
def load_main_api() -> ALL_APIS:
    return ALL_APIS(
        lang='www',
        family='nccommons',
        username=user_account_new.bot_username,
        password=user_account_new.bot_password,
    )


main_api = load_main_api()

wiki_NEW_API = main_api.NEW_API
wiki_MainPage = main_api.MainPage

NEW_API = main_api.NEW_API
MainPage = main_api.MainPage
CatDepth = main_api.CatDepth
