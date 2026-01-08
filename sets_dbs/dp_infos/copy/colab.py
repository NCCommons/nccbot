# prompt: Write code to create backup in SQL format of a SQLite 3 database named: fs_infos_duplict1.sqlite
# table 'infos', Columns: url, urlid, file
# use tqdm to print steps
# print total_rows of sqlite db
# write the chunk lines at once not one by one
# row['url'] and row['file'] may have charters like: (') or (") use escape_string to fix them
# from pymysql.converters import escape_string
# CREATE TABLE IF NOT EXISTS

import sqlite3
import pandas as pd
from tqdm import tqdm
from pymysql.converters import escape_string

# Connect to SQLite database
conn_sqlite = sqlite3.connect("fs_infos_duplict1.sqlite")

# Get total number of rows
total_rows = pd.read_sql_query("SELECT COUNT(*) FROM infos", conn_sqlite).iloc[0, 0]
print("Total rows in SQLite database:", total_rows)

# Create a file to store the SQL dump
with open("backup.sql", "w") as f:
    # Write table creation statement
    f.write("CREATE TABLE IF NOT EXISTS infos (url TEXT, urlid TEXT, file TEXT);\n")

    # Iterate over data in chunks and write INSERT statements
    chunk_size = 100000
    num_chunks = (total_rows // chunk_size) + 1
    # ---
    for i in tqdm(range(num_chunks), total=7083106):
        start = i * chunk_size
        end = (i + 1) * chunk_size
        df = pd.read_sql_query(f"SELECT * FROM infos LIMIT {start}, {chunk_size}", conn_sqlite)

        insert_statements = []
        for _, row in df.iterrows():
            urlid = row["urlid"]
            url = row["url"]
            # ---
            if url.find("'") > 0 or url.find('"') > 0:
                url = escape_string(row["url"])
            # ---
            file = row["file"]
            # ---
            if file.find("'") > 0 or file.find('"') > 0:
                file = escape_string(row["file"])
            # ---
            insert_statements.append(f"INSERT INTO infos (url, urlid, file) VALUES ('{url}', '{urlid}', '{file}');\n")

        # Write all insert statements for the chunk at once
        f.writelines(insert_statements)

# Close connection
conn_sqlite.close()


# !wget https://ncc.toolforge.org/fs_infos_duplict1.sqlite

# !huggingface-cli login --token ----------------
# !huggingface-cli upload Ibrahemqasim/radio_ncc backup.sql backup.sql
