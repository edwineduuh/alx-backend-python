import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL
)
""")

cursor.executemany("""
INSERT INTO users (name, email, age)
VALUES (?, ?, ?)
""", [
    ("Alice", "alice@example.com", 30),
    ("Bob", "bob@example.com", 24),
    ("Charlie", "charlie@example.com", 28)
])

conn.commit()
conn.close()
