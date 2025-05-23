import sqlite3
import functools

# ✅ Reuse from previous task: opens and closes DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# ✅ New decorator: manages DB transaction
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # ✅ Commit on success
            return result
        except Exception as e:
            conn.rollback()  # Roll back on error
            raise e
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id: int, new_email: str) -> None:
    with conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
### Update user's email with automatic connection and transaction handling
update_user_email(1, 'Crawford_Cartwright@hotmail.com')


