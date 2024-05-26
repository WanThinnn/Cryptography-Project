import mysql.connector
import os
import sys

# Thêm thư mục gốc vào PYTHONPATH để có thể import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def connect_to_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def fetch_users():
    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    connection.close()
    return users

def fetch_resources():
    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM resources")
    resources = cursor.fetchall()
    connection.close()
    return resources
