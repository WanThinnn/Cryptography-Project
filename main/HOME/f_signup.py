import bcrypt
from mysql.connector import connect
from PyQt6.QtWidgets import QMessageBox
from login_system import *

class SignupHandler:
    def __init__(self):
        self.connection = connect(
            host="company-database.clce6ae44hhz.ap-southeast-2.rds.amazonaws.com",
            user="admin",
            password="24122003",
            database="company_db"
        )
        self.login_instance = LoginSystem()

    def signup(self, username, password):
        return self.login_instance.sign_up(self.connection, username, password)




