""" """

import os
from pathlib import Path
from api_bots import printe

home_dir = os.getenv("HOME")
project = home_dir if home_dir else "I:/ncc"
main_dir = Path(project) / "ncc_data/ncc_jsons_dump"

studies_dir = main_dir / "studies"
studies_urls_to_files_dir = main_dir / "studies_urls_to_files"

printe.output(f"<<yellow>> studies_dir {studies_dir}")

printe.output(f"<<yellow>> studies_urls_to_files_dir {studies_urls_to_files_dir}")
