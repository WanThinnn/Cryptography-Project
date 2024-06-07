#db.py
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="company-database.clce6ae44hhz.ap-southeast-2.rds.amazonaws.com",
        user="admin",
        password="24122003",
        database="company_db"
    )
