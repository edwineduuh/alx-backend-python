#!/usr/bin/python3
import sqlite3
from itertools import islice

DB_PATH = 'user_data.db'

def stream_users_in_batches(batch_size):
    """Generator that yields batches of users from the database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM user_data")
    while True:
        batch = list(islice(cursor, batch_size))
        if not batch:
            conn.close()
            break
        yield [dict(row) for row in batch]

def batch_processing(batch_size):
    """Processes batches of users, filtering those over age 25"""
    for batch in stream_users_in_batches(batch_size):
        filtered_batch = [user for user in batch if user['age'] > 25]
        for user in filtered_batch:
            print(user)