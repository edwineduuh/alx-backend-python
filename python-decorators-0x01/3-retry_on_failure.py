import time
import sqlite3
import functools

# --- Decorator to connect to DB and pass connection to the wrapped function ---
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

# --- Retry decorator ---
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed with error: {e}")
                    attempt += 1
                    if attempt < retries:
                        time.sleep(delay)
                    else:
                        raise e
        return wrapper
    return decorator

# --- Function using both decorators ---
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# --- Run the function ---
users = fetch_users_with_retry()
print(users)
