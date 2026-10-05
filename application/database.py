import mysql.connector
from mysql.connector import Error


def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="lez$0812",
            database="airline_reservation_db"
        )

        if connection.is_connected():
            return connection

    except Error as e:
        print(f"Database connection error: {e}")

    return None