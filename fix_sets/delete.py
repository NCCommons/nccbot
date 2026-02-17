"""
python3 core8/pwb.py fix_sets/delete
"""

from fix_sets.ncc_api import CatDepth, post_ncc_params

fixed = CatDepth("Category:To delete", sitecode="www", family="nccommons", depth=0, ns=0, onlyns=0)

for x in fixed:
    params = {"action": "delete", "format": "json", "title": x, "reason": "Duplicate", "formatversion": "2"}
    # ---
    result = post_ncc_params(params, addtoken=True)
    # ---
    print(result)
