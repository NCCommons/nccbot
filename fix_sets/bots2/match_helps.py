"""

from fix_sets.bots2.match_helps import match_urlid, match_id # match_id(content, title)

"""

import re


def match_urlid(url):
    # ---
    url_id = ""
    # ---
    # find id from url like: https://prod-images-static.radiopaedia.org/images/(\d+)/.*?$
    mat = re.match(r"https://prod-images-static.radiopaedia.org/images/(\d+)/.*?$", url)
    if mat:
        url_id = mat.group(1)
    # ---
    return url_id


def match_id(content, title):
    # ---
    # * Image ID: [https://mdwiki.toolforge.org/images/1f1a1dd1cd3686f16594b05e17d72a.jpg 29774172]
    ma2 = re.findall(r"Image ID: \[[^[\]]+ (\d+)\]", content)
    # ---
    # match * Image ID: 10422592
    ma = re.findall(r"Image ID: (\d+)", content) or ma2
    img_id = ""
    # ---
    if ma:
        img_id = ma[0]
    # ---
    return img_id
