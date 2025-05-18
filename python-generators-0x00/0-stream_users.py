import mysql.connector
from dotenv import load_dotenv
import os
from typing import Generator, Dict

load_dotenv()  # Load environment variables from .env

def stream_users() -> Generator[Dict, None, None]:
    db_connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),                   
        user=os.getenv("DB_USER"),                   
        password=os.getenv("DB_PASSWORD"),            
        database=os.getenv("DB_NAME")                 
    )
    
    streams = db_connection.cursor(dictionary=True)
    streams.execute("SELECT * FROM user_data")
    
    for stream in streams:
        yield stream
    streams.close()
    db_connection.close()

