import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def paginate_users(page_size, offset):

    """Fetch a page of users starting from offset with page_size limit"""

    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "ALX_prodev")
    )

    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM user_data LIMIT %s OFFSET %s"      
    cursor.execute(query, (page_size, offset))
    rows = cursor.fetchall()
    return rows
        
def fetch_all_users_from_db():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME", "ALX_prodev")
        )
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM user_data"
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    finally:
        try:
            cursor.close()
            connection.close()
        except Exception:
            pass


def lazy_paginate(page_size):
    offset = 0

    while True:  
        page = paginate_users(page_size, offset)
        if not page: break
        yield from page  
        offset += page_size

