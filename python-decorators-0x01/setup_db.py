import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Drop existing table if needed
cursor.execute("DROP TABLE IF EXISTS users")

# Create table with an email column
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT
)
''')

# Insert some sample users
cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Alice", "alice@example.com"))
cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Bob", "bob@example.com"))

conn.commit()
conn.close()

print("✅ users table created and seeded.")
