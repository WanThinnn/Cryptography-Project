import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from login import Ui_LoginWindow
from signup import Ui_SignupWindow
from f_login import LoginHandler
from f_signup import SignupHandler
from ABAC.abac import Ui_MainWindow
from ABAC.classABAC import AttributeBasedAccessControl
from ABAC.fabac import *
from HOME.home_main import *

class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Login")
        self.db_handler = LoginHandler()
        self.ui.pushButton_signup.clicked.connect(self.open_signup_form)
        self.ui.pushButton_login.clicked.connect(self.login)

    
    
    def show_message(self, title, message, icon):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.exec()
        
    def open_signup_form(self):
        self.signup_window = SignupWindow()
        self.signup_window.show()
    
    def open_main_form(self, username):
        self.home_window = HomeWindows(username)
        self.home_window.show()
        self.hide()  # Ẩn cửa sổ đăng nhập khi mở cửa sổ chính
        
    def login(self):
        username = self.ui.lineEdit_username.text()
        password = self.ui.lineEdit_password.text()

        if username and password:
            if self.db_handler.login(username, password):
                # QMessageBox.information(None, "Đăng Nhập", "Đăng nhập thành công!")
                # if self.check_access(username, "view"):
                self.open_main_form(username)
            else:
                QMessageBox.information(None, "Đăng Nhập", "Đăng nhập thất bại, sai tên tài khoản hoặc mật khẩu!")
        else:
            QMessageBox.warning(None, "Lỗi", "Vui lòng điền đầy đủ thông tin")


class SignupWindow(QMainWindow):
    def __init__(self):
        super(SignupWindow, self).__init__()
        self.ui = Ui_SignupWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Signup")
        self.db_handler = SignupHandler()
        self.ui.pushButton_signup.clicked.connect(self.signup)

    def signup(self):
        username = self.ui.lineEdit_username.text()
        password = self.ui.lineEdit_password.text()
        password_2 = self.ui.lineEdit_password_2.text()
        if password != password_2:
            QMessageBox.warning(None, "Lỗi", "Mật khẩu không khớp!")
            return
        if username and password:
            if self.db_handler.signup(username, password):
                QMessageBox.information(None, "Đăng Ký", f"Đăng ký thành công tài khoản {username}!")
                # Đặt lại các ô nhập liệu về trống sau khi đăng ký thành công
                self.ui.lineEdit_username.setText("")
                self.ui.lineEdit_password.setText("")
                self.ui.lineEdit_password_2.setText("")
            else:
                QMessageBox.information(None, "Đăng Ký", "Đăng ký không thành công! Tài khoản đã tồn tại")
        else:
            QMessageBox.warning(None, "Lỗi", "Vui lòng điền đầy đủ thông tin")
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())
