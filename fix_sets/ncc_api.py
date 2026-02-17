"""

from fix_sets.ncc_api import ncc_MainPage
from fix_sets.ncc_api import CatDepth
from fix_sets.ncc_api import post_ncc_params

"""

from api_bots.page_ncc import NEW_API, CatDepth, ncc_MainPage

api_new = NEW_API()


def post_ncc_params(params, **kwargs):
    # ---
    result = api_new.post_params(params, **kwargs)
    # ---
    return result


__all__ = [
    "post_ncc_params",
    "ncc_MainPage",
    "CatDepth",
    "NEW_API",
    "api_new",
]
