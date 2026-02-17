"""
from fix_sets.bots.ddo_bot import ddo, remove_done
"""

import sys
from time import sleep

from fix_sets.bots.has_url import already_has_url
from fix_sets.lists.studies_fixed import studies_fixed_done
import logging
logger = logging.getLogger(__name__)

def make_tabs(ids):
    length = (len(ids) // 10) + 1
    # ---
    length = 1000
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(":")
        if arg == "le" and value.isdigit():
            length = int(value)
    # ---
    tabs = {}
    # ---
    for i in range(0, len(ids), length):
        num = i // length + 1
        # ---
        tabs[str(num)] = ids[i : i + length]
        # ---
        command = f"tfj run fix{num} --mem 1Gi --image python3.11 --command"
        command += ' "'
        # ---
        command += f"$HOME/local/bin/python3 c8/pwb.py fix_sets/new_all le:{length} get:{num} rev nodb"
        # ---
        lena = len(tabs[str(num)])
        # ---
        if lena != length:
            command += f" {lena}"
        # ---
        command += '"'
        # ---
        logger.info(command)
    # ---
    return tabs

def remove_done(taba):
    no_done = [x for x in taba if x not in studies_fixed_done]
    logger.info(f"\t\t ids after_done: <<yellow>>{len(no_done):,}")
    return no_done

def ddo(taba, spli=True):
    ids = taba
    # ---
    logger.info("<<green>> ----------------\nstart ddo:")
    # ---
    logger.info(f"Ids: <<yellow>>{len(ids):,},")
    # ---
    if "nodone" not in sys.argv:
        Done = studies_fixed_done
        # ---
        logger.info("\tworking after_done:, add 'nodone' to skip this..")
        # after_done = [x for x in ids if x not in Done]
        after_done = set(ids) - set(Done)
        after_done = list(after_done)
        # ---
        logger.info(f"\t\t ids after_done: <<yellow>>{len(after_done):,}")
        # ---
        ids = after_done
    # ---
    if "hasskip" not in sys.argv:
        logger.info(f"\n\t already_has_url: <<yellow>>{len(already_has_url):,}")
        # ---
        logger.info("\t\tworking after_has_urls:, add 'hasskip' to skip this..")
        # after_has_urls = [x for x in ids if x not in already_has_url]
        after_has_urls = set(ids) - set(already_has_url)
        after_has_urls = list(after_has_urls)
        # ---
        # logger.info(f"all ids: {len(ids)}, already_has_url:{len(already_has_url)}, after_has_urls: {len(after_has_urls)}")
        # ---
        logger.info(f"\t\t ids after_has_urls: <<yellow>>{len(after_has_urls):,}")
        # ---
        ids = after_has_urls
    # ---
    logger.info("<<yellow>> ----------------")
    if spli:
        tabs = make_tabs(ids)
        # ---
        for arg in sys.argv:
            arg, _, value = arg.partition(":")
            if arg == "get":
                ids = tabs[value]
                logger.info(f"work in {len(ids)} ids")
        del tabs
    # ---
    logger.info("<<green>> \n end ddo\n----------------")
    # ---
    sleep(2)
    # ---
    return ids
