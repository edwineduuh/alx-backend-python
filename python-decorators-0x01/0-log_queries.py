import sqlite3
import functools
from datetime import datetime  # ✅ this is now included as required

# ✅ Decorator to log SQL queries with a timestamp
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # ✅ Get the current time
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # ✅ Extract the query
        if args:
            query = args[0]
        elif 'query' in kwargs:
            query = kwargs['query']
        else:
            query = "No SQL query provided"

        # ✅ Log it with the timestamp
        print(f"[{now}] Executing SQL Query: {query}")

        # ✅ Call the original function
        return func(*args, **kwargs)
    
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# ✅ Sample function call to trigger the decorator
users = fetch_all_users(query="SELECT * FROM users")
