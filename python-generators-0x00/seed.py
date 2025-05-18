import mysql.connector
import csv
import uuid
import requests
import io
from decimal import Decimal
from dotenv import load_dotenv
import os
url = 'https://savanna.alxafrica.com/rltoken/kPrtJ_hN0TXKgEfwKY4vHg'


load_dotenv()
host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")
# 1. Connect to the databse
def connect_db():
    return mysql.connector.connect(
        host = host,
        user = user,
        password = password,
       
    )
# 2 Create database if it doesn't exist
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    connection.commit()
    
# 3. Connect to the database ALX_prodev
def connect_to_prodev():
    return mysql.connector.connect(
        host = host,
        user = user,
        password = password,
        database = database
    )
    
# 4. Create the table if it doesn't exist
def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(5,2) NOT NULL,
            INDEX (user_id)
            )
        """)
    connection.commit()
    
# 5. Insert data from csv file if it doesn't exist already
def insert_data(connection, data):
    cursor = connection.cursor()
    for row in data:
        user_id = str(uuid.uuid4())
        name, email, age = row
        cursor.execute("""
            SELECT COUNT(*) FROM user_data WHERE email = %s
        """, (email,))
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """, (user_id, name, email, Decimal(age)))
    connection.commit()

# 6. Generator to stream rows
def stream_user_data(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row

# 7. Read CSV data from a URL
def read_csv(url):
    response = requests.get(url)
    response.raise_for_status()  # raise error if URL fails
    csvfile = io.StringIO(response.text)
    reader = csv.reader(csvfile)
    next(reader)  # skip header
    return list(reader)


# 8. Main function to run everything

def main():
    conn = connect_db()
    create_database(conn)
    conn.close()

    prodev_conn = connect_to_prodev()
    create_table(prodev_conn)

    data_url = "https://savanna.alxafrica.com/rltoken/kPrtJ_hN0TXKgEfwKY4vHg"  
    data = read_csv(data_url)
    insert_data(prodev_conn, data)

    print("Streaming user_data rows:")
    for row in stream_user_data(prodev_conn):
        print(row)

    prodev_conn.close()
