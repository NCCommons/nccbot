"""

from fix_sets.bots2.filter_ids import filter_no_title

"""

# import sys

from fix_mass.files import studies_titles, studies_titles2
import logging
logger = logging.getLogger(__name__)

def filter_no_title(ids):
    # ---
    ss_tt = studies_titles.copy()
    ss_tt.update(studies_titles2)
    # ---
    if not ids:
        logger.info("\t<<red>> filter_no_title, no ids. return {}")
        return {}
    # ---
    ids_to_titles = {study_id: ss_tt[study_id] for study_id in ids if study_id in ss_tt}
    # ---
    if len(ids_to_titles) != len(ids):
        ids_no_title = [k for k in ids if k not in ids_to_titles]
        # ---
        logger.info(f" remove ids_no_title: {len(ids_no_title):,}")
        print("\t\t", ", ".join(ids_no_title))
    # ---
    logger.info(f"<<green>> len of ids: {len(ids):,}, after filter_no_title: {len(ids_to_titles):,}")
    # ---
    return ids_to_titles
