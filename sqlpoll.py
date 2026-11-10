import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), "poll.db")

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS votes (
    film TEXT NOT NULL,
    option TEXT NOT NULL,
    count INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (film, option)
)
""")

# Check whether the old database needs migration
cursor.execute("PRAGMA table_info(votes)")
columns = [column[1] for column in cursor.fetchall()]

if "film" not in columns:
    print("Migrating existing Born Free votes...")

    cursor.execute("ALTER TABLE votes RENAME TO votes_old")

    cursor.execute("""
    CREATE TABLE votes (
        film TEXT NOT NULL,
        option TEXT NOT NULL,
        count INTEGER NOT NULL DEFAULT 0,
        PRIMARY KEY (film, option)
    )
    """)

    cursor.execute("SELECT option, count FROM votes_old")

    for option, count in cursor.fetchall():
        cursor.execute("""
        INSERT INTO votes (film, option, count)
        VALUES ('born-free', ?, ?)
        """, (option, count))

# Initialise both film polls
films = ["born-free", "emanzini"]
options = ["loved", "good", "notforme"]

for film in films:
    for option in options:
        cursor.execute("""
        INSERT OR IGNORE INTO votes (film, option, count)
        VALUES (?, ?, 0)
        """, (film, option))

conn.commit()
conn.close()

print("Blackdot poll database successfully configured!")