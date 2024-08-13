import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            database="fitness_center_db",
            user="root",
            password="Czmpdrdv123!",
            host="localhost",
        )
        print("Connected to database")
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None