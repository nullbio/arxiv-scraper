import logging
import sqlite3
from typing import Tuple


class SQL:
    def __init__(self, db_file: str, logger: logging.Logger):
        # set up sqlite connection and db
        sqlite3.enable_callback_tracebacks(True)
        # Connect to the SQLite database
        self.db = sqlite3.connect(db_file)
        self.db.row_factory = sqlite3.Row
        self.cursor = self.db.cursor()
        # Set up the database
        try:
            with open("init.sql", "r") as sql_file:
                sql_script = sql_file.read()

            self.cursor.executescript(sql_script)
        except sqlite3.Error as e:
            logger.error(
                "Could not set up database, err: %s, err_name: %s, err_code: %s",
                e,
                e.sqlite_errorname,
                e.sqlite_errorcode,
            )
            exit(1)

    def close(self):
        self.cursor.close()
        self.db.close()

    # return a list of Category objects, filled from the database
    def get_categories(self):
        categories = []
        self.cursor.execute("SELECT category, end_year FROM categories")
        for row in self.cursor:
            categories.append(
                {"category": row["category"], "end_year": row["end_year"]}
            )
        return categories

    # return a list of archive urls that have been fully scraped
    def get_finished_archive_urls(self):
        self.cursor.execute(
            """SELECT archive_url FROM categories_monthly_archive
            WHERE collected_entries >= total_entries AND total_entries > 0"""
        )

        return [row["archive_url"] for row in self.cursor]
