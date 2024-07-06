import mysql.connector

mydb = mysql.connector.connect(
    host="company-database.clce6ae44hhz.ap-southeast-2.rds.amazonaws.com",
    user="admin",
    password="24122003",
    database="company_db"
)

def insert(username, password_hash):
    try:
        mycursor = mydb.cursor()
        mycursor.callproc('AddUser', [username, password_hash])
        mydb.commit()  # Ensure to commit the transaction
        mycursor.close()
        print("Account created!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if mycursor:
            mycursor.close()

def getUserPWHash(username):
    try:
        mycursor = mydb.cursor()
        mycursor.callproc('GetPWHash', [username])
        for result in mycursor.stored_results():
            data = result.fetchone()
        return data[0] if data else None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if mycursor:
            mycursor.close()
