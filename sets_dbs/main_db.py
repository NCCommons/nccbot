#!/usr/bin/python3
"""

python3 core8/pwb.py main_db


from sets_dbs.main_db import DbClass

class MyDb(DbClass):

    def __init__(self):
        # ---
        self.table_name = ''
        self.create_table_query = '''
            CREATE TABLE IF NOT EXISTS `cats` (
            `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
            `old` text NULL,
            `new` text NOT NULL,
            `done` text NULL,
            `reson` text NULL
            );
            '''
        # ---
        super().__init__(self.table_name, self.create_table_query)
        # ---
        # self.execute(query, params=None, get_data=False)
        # self.executemany(query, params=None)
        # self.get_all()
        # self.do_query(query, values=None, get_data=False)

"""
import configparser
import logging
import os
import sys

import pymysql
import pymysql.cursors
from pywikibot import config

logger = logging.getLogger(__name__)
# ---
conversions = pymysql.converters.conversions
conversions[pymysql.FIELD_TYPE.DATE] = lambda x: str(x)
# ---
can_use_sql_db = {1: True}
# ---
main_args = {
    "host": "",
    "db": "",
    "charset": "utf8mb4",
    "use_unicode": True,
    "autocommit": True,
}
# ---
home = os.getenv("HOME")
# ---
if "localhost" in sys.argv or not home:
    main_args["host"] = "127.0.0.1"
    main_args["db"] = "ncc"
    credentials = {"user": "root", "password": "root11"}
else:
    db_username = config.db_username
    db_password = config.db_password
    # ---
    if config.db_connect_file is None:
        credentials = {"user": db_username, "password": db_password}
    else:
        credentials = {"read_default_file": config.db_connect_file}
        # ---
        conf = configparser.ConfigParser()
        # ---
        conf.read(credentials["read_default_file"])
        # ---
        db_username = conf["client"]["user"]
        db_password = conf["client"]["password"]
    # ---
    main_args["db"] = f"{db_username}__ncc"
    main_args["host"] = "tools.db.svc.wikimedia.cloud"
    # ---
    credentials = {"user": db_username, "password": db_password}


class DbClass:
    """
    function
    """

    def __init__(self, table_name, create_table_query):
        """
        function
        """
        # ---
        self.connection = None
        self.table_name = table_name
        self.create_table_query = create_table_query
        # ---
        args = main_args.copy()
        args["cursorclass"] = pymysql.cursors.DictCursor
        # ---
        if conversions:
            args["conv"] = conversions
        # ---
        if "nodb" in sys.argv:
            return
        # ---
        try:
            self.connection = pymysql.connect(**args, **credentials)
        except Exception as e:
            logger.exception('Exception:', exc_info=True)
        # ---
        self.create_database_table()

    def execute(self, query, params=None, get_data=False):
        if not self.connection:
            return []
        # ---
        # with self.connection as conn, conn.cursor() as cursor:
        with self.connection.cursor() as cursor:
            # skip sql errors
            try:
                cursor.execute(query, params)
                if not get_data:
                    return True

            except Exception as e:
                logger.exception('Exception:', exc_info=True)
                # ---
                if get_data:
                    return []
                else:
                    return False

            try:
                results = cursor.fetchall()
            except Exception as e:
                logger.exception('Exception:', exc_info=True)
                return []

        return results

    def executemany(self, query, params=None):
        if not self.connection:
            return []
        # with self.connection as conn, conn.cursor() as cursor:
        with self.connection.cursor() as cursor:
            # skip sql errors
            try:
                cursor.executemany(query, params)
                return True

            except Exception as e:
                logger.exception('Exception:', exc_info=True)
                return False

    def create_database_table(self):
        if not self.connection:
            return []
        """
        function
        """
        # ---
        self.execute(self.create_table_query)

    def do_query(self, query, values=None, get_data=False):
        if not self.connection:
            return []
        """
        function
        """
        # ---
        results = self.execute(query, values, get_data=True)
        # ---
        if get_data:
            list_accumulator = []
            # ---
            for item in results:
                list_accumulator.append({k: item[k] for k in item.keys()})
            # ---
            return list_accumulator
        # ---
        return True

    def get_all(self):
        if not self.connection:
            return []
        """
        function
        """
        qua = f"SELECT * FROM {self.table_name};"
        # ---
        data = self.do_query(qua, get_data=True)
        # ---
        return data
