import mysql.connector
from mysql.connector import Error
import json

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="company-database.clce6ae44hhz.ap-southeast-2.rds.amazonaws.com",
            user="admin",
            password="24122003",
            database="company_db"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def close_db_connection(connection):
    if connection.is_connected():
        connection.close()

def call_add_policy_procedure(policy):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.callproc('AddPolicy', (
                policy["uid"],
                policy["description"],
                policy["effect"],
                json.dumps(policy["rules"]),
                json.dumps(policy["targets"])
            ))
            connection.commit()
            print("Policy added to database successfully via procedure.")
        except Error as e:
            print(f"Error calling AddPolicy procedure: {e}")
        finally:
            cursor.close()
            close_db_connection(connection)
