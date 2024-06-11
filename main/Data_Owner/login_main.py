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

    def check_access(self, username, resource_type):
        abac = AttributeBasedAccessControl()

        # Lấy thông tin nhân viên từ MySQL
        employee = abac.get_employee_attributes(username)
        if not employee:
            print(f"No employee found with username {username}")
            return

        # Tạo yêu cầu truy cập
        request_access_format = {
            "subject": {
                "id": username,
                "attributes": {
                    "role": employee['role'],
                    "department": employee['department'],
                    "position": employee['position'],
                }
            },
            "resource": {
                "id": "2",
                "attributes": {
                    "type": resource_type,
                    "department": employee['department']  # Ensure the resource department matches the user's department
                }
            },
            "action": {
                "id": "3",
                "attributes": {
                    "method": "upload"
                }
            },
            "context": {}
        }

        if abac.is_request_allowed(request_access_format):
            print("Allowed")
            return True
            # self.show_message("Access Granted", "Your access request has been approved.", QMessageBox.Icon.Information)
        else:
            print("Denied")
            self.show_message("Access Denied", "You do not have permission to access this resource.", QMessageBox.Icon.Warning)
            return False

    
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
        self.hide()
        
    def login(self):
        username = self.ui.lineEdit_username.text()
        password = self.ui.lineEdit_password.text()

        if username and password:
            if self.db_handler.login(username, password):
                # QMessageBox.information(None, "Đăng Nhập", "Đăng nhập thành công!")
                if self.check_access(username, "all"):
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
