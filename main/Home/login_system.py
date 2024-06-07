import bcrypt
import mysql.connector



def insert(mydb, username, password_hash):
    try:
        mycursor = mydb.cursor()
        mycursor.callproc('AddUser', [username, password_hash])
        mydb.commit()  # Ensure to commit the transaction
        mycursor.close()
        return True
    except mysql.connector.Error as err:
        return False
    finally:
        if mycursor:
            mycursor.close()

def getUserPWHash(mydb, username):
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

class LoginSystem:
    @staticmethod
    def promptForCreds():
        username = input("Nhập tên người dùng: ")
        password = input("Nhập mật khẩu: ")
        return username, password

    @staticmethod
    def passwordHashing(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14)).decode('utf-8')

    @staticmethod
    def validateCredentials(password, password_hash):
        return bcrypt.checkpw(password.encode('utf8'), password_hash.encode('utf8'))

    def sign_up(self, connection, username, password):
        return insert(connection, username, self.passwordHashing(password))

    def login(self,connection, username, password):
        password_hash = getUserPWHash(connection, username)
        if password_hash:
            return self.validateCredentials(password, password_hash)
        return False