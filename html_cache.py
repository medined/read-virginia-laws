"""Cache HTML Responses"""

from pprint import pprint
from sqlite3 import OperationalError
import logging
import sqlite3 as sl

logger = logging.getLogger(__name__)

class HtmlCache:
    """Cache HTML responses."""

    def __init__(self, database_filespec='rvl.db') -> None:
        self.database_filespec = database_filespec
        self.connection = sl.connect(self.database_filespec)
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS html_responses (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                flag_error INTEGER,
                response TEXT
            );
        """)

    def print_all_rows(self):
        """Display all rows in the database."""
        print('--- db start ---------------')
        data = self.connection.execute("SELECT * FROM html_responses")
        for row in data:
            pprint(row)
        print('--- db end -----------------')


    # make sure the URL does not exist in the database
    # before inserting it.
    def insert(self, url, response, flag_error) -> None:
        """Insert a single record."""
        sql = "INSERT INTO html_responses (url, response, flag_error) values(?, ?, ?)"
        data = (url, response, flag_error)
        with self.connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql, data)
            except OperationalError as exeception:
                logger.fatal("SQL: %s", sql)
                raise exeception
            conn.commit()

    def exists(self, url):
        """Check that a record exists using the url as the key."""
        sql = f"SELECT * FROM html_responses WHERE url = '{url}'"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        return True if row else False

    def read(self, url):
        """Get the original response from the cache for a given URL."""
        sql = f"SELECT flag_error, response FROM html_responses WHERE url = '{url}'"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        if not row:
            return False, None
        flag_error, response = row
        return flag_error, response
