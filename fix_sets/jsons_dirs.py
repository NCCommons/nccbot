"""

from fix_sets.jsons_dirs import get_study_dir, jsons_dir

"""
import os
from pathlib import Path
from api_bots import printe

home_dir = os.getenv("HOME")
project = home_dir if home_dir else "I:/ncc"
jsons_dir = Path(project) / "ncc_jsons_dump/fix_mass_jsons"

if not jsons_dir.exists():
    jsons_dir.mkdir()

st_ref_infos = jsons_dir / "studies_t"

if not st_ref_infos.exists():
    st_ref_infos.mkdir(parents=True)


def get_study_dir(study_id):
    study_id_dir = st_ref_infos / study_id

    if not study_id_dir.exists():
        printe.output(f"<<yellow>> create: {study_id_dir}")
        study_id_dir.mkdir(parents=True)
    return study_id_dir
