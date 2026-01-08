"""
from logs_fix.files import has_url_dir, move_text_dir
"""
from pathlib import Path
import os

home_dir = os.getenv("HOME")
project = home_dir if home_dir else "I:/ncc"
logs_fix_dir = Path(project) / "ncc_data/logs_fix"

has_url_dir = logs_fix_dir / "has_url"
move_text_dir = logs_fix_dir / "move_text"
