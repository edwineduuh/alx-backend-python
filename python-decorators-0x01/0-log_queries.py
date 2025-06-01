import sqlite3
import functools

# ✅ Step 1: Define the decorator
def log_queries(func):
    # use functools.wraps to preserve function metadata like name, docstring, etc.
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # ✅ Step 2: Extract the SQL query
        # We assume the SQL query is the first argument (positional)
        if args:
            print(f"SQL Query: {args[0]}")
        elif 'query' in kwargs:
            print(f"SQL Query: {kwargs['query']}")
        else:
            print("No SQL query found.")

        # ✅ Step 3: Call the original function
        return func(*args, **kwargs)
    
    return wrapper

# ✅ Step 4: Apply the decorator to a function that runs a SQL query
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')  # connect to SQLite database
    cursor = conn.cursor()
    cursor.execute(query)              # run the SQL query
    results = cursor.fetchall()       # fetch all results
    conn.close()                      # close the connection
    return results

# ✅ Step 5: Call the function with a query
users = fetch_all_users(query="SELECT * FROM users")
