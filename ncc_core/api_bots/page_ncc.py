"""

from api_bots.page_ncc import ncc_MainPage, ncc_NEW_API

"""

import functools
import os
from dotenv import load_dotenv
load_dotenv()

from newapi import AllAPIS

username = os.getenv("WIKIPEDIA_BOT_USERNAME", "")
password = os.getenv("WIKIPEDIA_BOT_PASSWORD", "")


@functools.lru_cache(maxsize=1)
def load_main_api() -> AllAPIS:
    return AllAPIS(lang="www", family="nccommons", username=username, password=password)


main_api = load_main_api()

ncc_NEW_API = main_api.NewApi  # noqa: N816
ncc_MainPage = main_api.MainPage  # noqa: N816

NewApi = main_api.NewApi
MainPage = main_api.MainPage
CatDepth = main_api.CatDepth
