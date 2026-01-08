"""
from ncc_jsons.dir_studies_bot import studies_dir, studies_urls_to_files_dir

"""
import os
from pathlib import Path
from api_bots import printe

home_dir = os.getenv("HOME")
project = home_dir if home_dir else "I:/ncc"
main_dir = Path(project) / "ncc_jsons_dump"

# main_dir = Path(__file__).parent
# ---
# studies_dir = Path("/data/project/ncc/nccbot/ncc_jsons/studies")
studies_dir = main_dir / "studies"
studies_urls_to_files_dir = main_dir / "studies_urls_to_files"

printe.output(f"<<yellow>> studies_dir {studies_dir}")
# ---
# if not os.path.exists(studies_dir):
#     printe.output(f"<<red>> studies_dir {studies_dir} not found")
#     studies_dir = Path("I:/ncc/nccbot/ncc_jsons/studies")
#     printe.output(f"<<red>> studies_dir set to {studies_dir}")

printe.output(f"<<yellow>> studies_urls_to_files_dir {studies_urls_to_files_dir}")
