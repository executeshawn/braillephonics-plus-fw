import sqlite3

conn = sqlite3.connect("nfc_tags.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE nfc_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT UNIQUE NOT NULL,
    symbol TEXT,
    type TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

conn.commit()
conn.close()

print("Database created successfully.")