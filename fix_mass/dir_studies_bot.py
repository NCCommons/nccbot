""" """

import os
from pathlib import Path

import logging
logger = logging.getLogger(__name__)

home_dir = os.getenv("HOME")
project = home_dir if home_dir else "I:/ncc"
main_dir = Path(project) / "ncc_data/ncc_jsons_dump"

studies_dir = main_dir / "studies"
studies_urls_to_files_dir = main_dir / "studies_urls_to_files"

logger.info(f"<<yellow>> studies_dir {studies_dir}")

logger.info(f"<<yellow>> studies_urls_to_files_dir {studies_urls_to_files_dir}")
