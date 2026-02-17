# prompt: Write code to create backup in SQL format of a SQLite 3 database named: fs_infos_duplict1.sqlite
# table 'infos'
# Columns: url text, urlid text, file text
# use tqdm to print steps
# print total_rows of sqlite db
# write the chunk lines at once not one by one

import sqlite3

import pandas as pd
from tqdm import tqdm

# Connect to SQLite database
conn_sqlite = sqlite3.connect("fs_infos_duplict1.sqlite")

# Get total number of rows
total_rows = pd.read_sql_query("SELECT COUNT(*) FROM infos", conn_sqlite).iloc[0, 0]
print("Total rows in SQLite database:", total_rows)

# Create a file to store the SQL dump
with open("backup.sql", "w") as f:
    # Write table creation statement
    f.write("CREATE TABLE infos (url TEXT, urlid TEXT, file TEXT);\n")

    # Iterate over data in chunks and write INSERT statements
    chunk_size = 100000
    num_chunks = (total_rows // chunk_size) + 1
    for i in tqdm(range(num_chunks), total=7083106):
        start = i * chunk_size
        end = (i + 1) * chunk_size
        df = pd.read_sql_query(f"SELECT * FROM infos LIMIT {start}, {chunk_size}", conn_sqlite)
        insert_statements = df.apply(
            lambda row: f"INSERT INTO infos (url, urlid, file) VALUES ('{row['url']}', '{row['urlid']}', '{row['file']}');\n",
            axis=1,
        )
        f.writelines(insert_statements)

# Close connection
conn_sqlite.close()
