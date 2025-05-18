import mysql.connector
import os
from dotenv import load_dotenv
from typing import Generator, List, Dict

load_dotenv()

def stream_users_in_batches(batch_size: int) -> Generator[List[Dict], None, None]:
    db_connection = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "ALX_prodev")
    )

    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    batch = []
    for row in cursor:
        batch.append(row)
        if len(batch) == batch_size:
            yield batch
            batch = []

    # Yield the last batch if not empty
    if batch:
        yield batch

    cursor.close()
    db_connection.close()

def batch_processing(batch_size: int) -> None:
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user["age"] > 25:
                print(user)
