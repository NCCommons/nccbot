"""
from images_path import atlas_images_path
"""

import os
from pathlib import Path

home_dir = os.getenv("HOME")
project = home_dir if home_dir else "I:/ncc"
atlas_images_path = Path(project) / "ncc_data/atlas_images"
