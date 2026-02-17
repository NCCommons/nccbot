"""
python3 nccbot/sets_dbs/dp_infos/copy/sql_format_to_mysql.py
INSERT INTO infos (url, urlid, file) VALUES ('https://prod-images-static.radiopaedia.org/images/53744263/IMG-0001-00076.jpg', '53744263', 'File:Hangman's fracture (Radiopaedia 83504-98605 Axial 9).jpg');
"""

import os
import sys
from pathlib import Path

import pymysql
from tqdm import tqdm

# wget https://huggingface.co/Ibrahemqasim/radio_ncc/resolve/main/backup_no_duplicates.sql -O ~/public_html/adminer.sql

home_dir = os.getenv("HOME")
project = home_dir if home_dir else "I:/ncc"
Dir = Path(project) / "ncc_data/sets_dbs/dp_infos/copy"

password = ""
user = ""

for arg in sys.argv:
    arg, _, value = arg.partition(":")
    if arg == "user":
        user = value
    elif arg == "password":
        password = value

filepath = Dir / "adminer.sql"
host = "tools.db.svc.wikimedia.cloud"
db_name = f"{user}__ncc"


def fix_line(line):
    # INSERT INTO infos (url, urlid, file) VALUES ('https://prod-images-static.radiopaedia.org/images/53744263/IMG-0001-00076.jpg', '53744263', 'File:Hangman's fracture (Radiopaedia 83504-98605 Axial 9).jpg');
    if line.count("'") == 6:
        return line
    # ---
    if line.count("'") > 6:
        line = line.replace("('", '("').replace("')", '")').replace("', '", '", "')
    # ---
    return line


def insert_data_chunked_new(filepath, db_name, host, user, password):
    """
    filepath: path to the SQL file
    db_name: name of the database
    host: database host
    user: database user
    password: database password
    """
    # Establish database connection
    connection = pymysql.connect(host=host, user=user, password=password, db=db_name)
    cursor = connection.cursor()
    done = 0
    bad = 0
    errors = 0
    # Read SQL file in chunks and extract INSERT statements
    with open(filepath, "r") as f:
        # ---
        for line in tqdm(f, total=7083106):
            line = line.strip()
            # ---
            lista = []
            # ---
            if line.endswith(";") and line.lower().startswith("insert into infos"):
                # line = fix_line(line)
                lista.append(line)
                if len(lista) == 10000:
                    print("10000...")
                    # ---
                    qua = """
                        INSERT INTO infos (url, urlid, file)
                        values (%s, %s, %s)
                        """
                    # ---
                    liso = []
                    for al in lista:
                        al = al.replace("INSERT INTO infos (url, urlid, file) VALUES (", "").replace(");", "")

                        liso.append(tuple(al.split(",")))
                    # ---
                    try:
                        cursor.executemany(qua, liso)
                        connection.commit()
                        done += len(lista)
                    except Exception as e:
                        print(f"Error inserting data: {e}")
                        # print(line)
                        errors += 1
                        for al in lista:
                            try:
                                cursor.execute(al)
                                connection.commit()
                                done += 1
                            except Exception as e:
                                errors += 1

                    lista = []
            else:
                bad += 1

    # Close database connection
    cursor.close()
    connection.close()
    print("Data inserted successfully!")
    print(f"Total errors: {errors:,}")
    print(f"Total rows inserted: {done:,}")
    print(f"Total bad lines: {bad:,}")


def insert_data_chunked(filepath, db_name, host, user, password):
    """
    filepath: path to the SQL file
    db_name: name of the database
    host: database host
    user: database user
    password: database password
    """
    # Establish database connection
    connection = pymysql.connect(host=host, user=user, password=password, db=db_name)
    cursor = connection.cursor()
    done = 0
    bad = 0
    errors = 0
    # Read SQL file in chunks and extract INSERT statements
    with open(filepath, "r") as f:
        # ---
        for line in tqdm(f, total=7083106):
            line = line.strip()
            # ---
            if line.endswith(";") and line.lower().startswith("insert into infos"):
                try:
                    cursor.execute(line)
                    connection.commit()
                    done += 1
                except Exception as e:
                    errors += 1

            else:
                bad += 1

    # Close database connection
    cursor.close()
    connection.close()
    print("Data inserted successfully!")
    print(f"Total errors: {errors:,}")
    print(f"Total rows inserted: {done:,}")
    print(f"Total bad lines: {bad:,}")


# Call the function to insert data
insert_data_chunked(filepath, db_name, host, user, password)
