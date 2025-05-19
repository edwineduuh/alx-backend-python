#!/usr/bin/python3
import sqlite3
import os

DB_PATH = r'C:\Users\LENOVO T14\alx-backend-python\python-generators-0x00\user_data.db'

def create_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute('''
        CREATE TABLE IF NOT EXISTS user_data (
            user_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL
        )
        ''')

        users = [
            # your sample data here
        ]

        c.executemany('INSERT OR IGNORE INTO user_data VALUES (?, ?, ?, ?)', users)
        conn.commit()
        print(f"Database created at {DB_PATH} with {len(users)} sample users.")
    except Exception as e:
        print(f"Error creating database: {e}")
    finally:
        conn.close()

def stream_users():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM user_data")
    while True:
        user = cursor.fetchone()
        if user is None:
            conn.close()
            break
        yield dict(user)

if __name__ == '__main__':
    create_db()