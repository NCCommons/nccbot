"""
from mass.radio.jsons_bot import radio_jsons_dir
(all_ids|authors|cases_cats|cases_count|cases_dup|cases_in_ids|ids|infos|PD_medical_pages|systems|to_work|url_to_sys|urls_to_get_info|urls)\.json

"""

from pathlib import Path

radio_jsons_dir = Path(__file__).parent / "jsons"
