import sqlite3

conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_data';")
table_exists = cursor.fetchone()
print(f"user_data table exists: {table_exists is not None}")

conn.close()
