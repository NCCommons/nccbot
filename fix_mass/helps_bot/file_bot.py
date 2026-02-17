"""

from fix_mass.helps_bot.file_bot import from_cach, dumpit

"""

import json
import sys
from pathlib import Path

import logging
logger = logging.getLogger(__name__)

def from_cach(file):
    if "nocach" in sys.argv:
        return {}
    file = Path(file)
    if file.exists():
        try:
            return json.loads(file.read_text())
        except Exception as e:
            logger.info(f"<<red>> from_cach: {file} error: {e}")
    return {}

def dumpit(data, file):
    file = Path(file)
    if "nodump" in sys.argv:
        return
    # ---
    if not data:
        logger.info(f"<<yellow>> No data to dump to file: {file}")
        return
    # ---
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
            logger.info(f"<<green>> Successfully write {len(data)} to file: {file}")

    except Exception as e:
        logger.info(f"<<red>> Error writing to file {file}: {str(e)}")
