# services/database.py

import sqlite3

class Database:

    def __init__(self, db_file="data/nfc_tags.db"):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def get_symbol(self, uid):

        uid_str = ''.join([format(i, '02X') for i in uid])

        self.cursor.execute(
            "SELECT symbol FROM nfc_tags WHERE uid=?",
            (uid_str,)
        )

        result = self.cursor.fetchone()

        return result[0] if result else None