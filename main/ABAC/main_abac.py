import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from abac import Ui_MainWindow
from classABAC import AttributeBasedAccessControl
from fabac import *

class MainWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Main Window")
        self.ui.lbUsername.setText(f"Welcome {username}")  # Hiển thị tên người dùng
        self.username = username  # Lưu tên người dùng
        self.ui.btnOK.clicked.connect(self.on_ok_clicked)
        self.db_handler = ProcessMongoDBCloud()
        
        self.ui.cbResource.addItems(self.db_handler.get_tables())

    def on_ok_clicked(self):
        selected_resource = self.ui.cbResource.currentText()  # Đảm bảo truy cập đúng cbResource
        print(f"Selected resource: {selected_resource}")
        # Gọi phương thức kiểm tra truy cập từ fabac.py
        self.check_access(self.username, selected_resource)

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
                    "method": "view"
                }
            },
            "context": {}
        }

        if abac.is_request_allowed(request_access_format):
            print("Allowed")
            self.show_message("Access Granted", "Your access request has been approved.", QMessageBox.Icon.Information)
        else:
            print("Denied")
            self.show_message("Access Denied", "You do not have permission to access this resource.", QMessageBox.Icon.Warning)

    def show_message(self, title, message, icon):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    username = "admin"  # Thay thế bằng tên người dùng thực tế sau khi đăng nhập
    main_window = MainWindow(username)
    main_window.show()
    sys.exit(app.exec())
