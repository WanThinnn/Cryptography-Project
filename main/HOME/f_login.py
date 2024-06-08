from mysql.connector import connect
from PyQt6.QtWidgets import QMessageBox
from signup import Ui_SignupWindow
from login_system import *



class LoginHandler:
    def __init__(self):
        self.connection = connect(
            host="company-database.clce6ae44hhz.ap-southeast-2.rds.amazonaws.com",
            user="admin",
            password="24122003",
            database="company_db"
        )
        self.signup_form = Ui_SignupWindow()
        self.login_instance = LoginSystem()
        
    def login(self, username, password):
        return self.login_instance.login(self.connection, username, password)
    
