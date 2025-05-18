
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def stream_user_ages():
    
    """ Fetch and return age of users from the database one at a time. """
    connection = mysql.connector.connect(
        
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "ALX_prodev")
    )
    
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    
    for row in cursor:  
        yield row['age']
    cursor.close()
    connection.close()

def calculate_average_age():
    
    total_age = 0
    count = 0
    for age in stream_user_ages():  
        total_age += age
        count += 1
    average = total_age / count if count else 0
    print(f"Average age of users: {average}")
    
if __name__ == "__main__":
    
    calculate_average_age()


