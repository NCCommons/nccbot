"""
# ---
from api_bots import user_account_new
# ---
username = user_account_new.bot_username     #user_account_new.my_username
password = user_account_new.bot_password     #user_account_new.my_password      #user_account_new.mdwiki_pass
lgpass_enwiki   = user_account_new.lgpass_enwiki
# ---
"""
import configparser

from pathlib import Path

Dir = str(Path(__file__).parents[0])

dir2 = Dir.replace("\\", "/")
dir2 = dir2.split("/ncc/")[0] + "/ncc"

config = configparser.ConfigParser()
config.read(f"{dir2}/confs/user.ini")

bot_username = config["DEFAULT"]["botusername"]
bot_password = config["DEFAULT"]["botpassword"]
