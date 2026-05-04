"""

from api_bots.page_md import load_main_api

"""

import functools
import os
from dotenv import load_dotenv
from newapi import AllAPIS

load_dotenv()


my_username = os.getenv("MDWIKI_HIMO_USERNAME", "")
mdwiki_pass = os.getenv("MDWIKI_HIMO_PASSWORD", "")


@functools.lru_cache(maxsize=1)
def load_main_api() -> AllAPIS:
    return AllAPIS(lang="www", family="mdwiki", username=my_username, password=mdwiki_pass)


main_api = load_main_api()

NewApi = main_api.NewApi
MainPage = main_api.MainPage
