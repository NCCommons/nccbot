# prompt: Write code to dump the infos table from a SQLite 3 database named: fs_infos_duplict1.sqlite
# Columns: url text, urlid text, file text
# and save rows to pymysql database name: db, Host: host, User:user, Password: Password
# show steps using tqdm

import os
import configparser
import sqlite3
import pandas as pd
from sqlalchemy import create_engine
from tqdm import tqdm
from pathlib import Path

home_dir = os.getenv("HOME")
project = home_dir if home_dir else "I:/ncc"
Dir = Path(project) / "ncc_data/sets_dbs/dp_infos/copy"

try:
    path_db_1 = Dir / "fs_infos_duplict1.sqlite"
except:
    path_db_1 = "fs_infos_duplict1.sqlite"


def get_user():
    # ---
    from pywikibot import config

    # ---
    if config.db_connect_file is None:
        user = config.db_username
        password = config.db_password
    else:
        credentials = {"read_default_file": config.db_connect_file}
        # ---
        conf = configparser.ConfigParser()
        # ---
        conf.read(credentials["read_default_file"])
        # ---
        user = conf["client"]["user"]
        password = conf["client"]["password"]
    # ---
    return password, user


# Connect to MySQL database
def db_host():
    # ---
    password, user = get_user()
    # ---
    host = "tools.db.svc.wikimedia.cloud"
    db_name = f"{user}__ncc"
    # ---
    home = os.getenv("HOME")
    # ---
    if not home:
        host = "127.0.0.1"
        user = "root"
        password = "root11"
        db_name = "ncc"
    # ---
    conn_mysql = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{db_name}")
    return conn_mysql


conn_mysql = db_host()

# Define database paths
# Connect to SQLite database
conn_sqlite = sqlite3.connect(path_db_1)

# Read data from SQLite
df = pd.read_sql_query("SELECT * FROM infos", conn_sqlite)

# Write data to MySQL in chunks with progress bar
chunk_size = 10000
num_chunks = (len(df) // chunk_size) + 1

for i in tqdm(range(num_chunks), total=7083106):
    start = i * chunk_size
    end = (i + 1) * chunk_size
    df.iloc[start:end].to_sql("infos", con=conn_mysql, if_exists="append", index=False)

# Close connections
conn_sqlite.close()
conn_mysql.dispose()
