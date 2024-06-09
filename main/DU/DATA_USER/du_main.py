import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QCheckBox, QVBoxLayout, QSizePolicy, QMessageBox
from DATA_USER.du_gui import DU_Ui_MainWindow
from PyQt6.QtGui import QIcon
from DATA_USER.du_functions import DatabaseHandler
from ABAC.abac import Ui_MainWindow
from ABAC.classABAC import AttributeBasedAccessControl
from ABAC.fabac import *

class AES_MainWindow(QMainWindow):
    def __init__(self, username):
        super(AES_MainWindow, self).__init__()
        self.ui = DU_Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Data User App: " + username)
        #self.setWindowIcon(QIcon('/Users/wanthinnn/Downloads/nekocoffee.icns')) 
        self.db_handler = DatabaseHandler(self.ui)
        self.username = username
        self.ui.comboBox_table.addItems(self.db_handler.get_tables())
        self.ui.comboBox_table.currentTextChanged.connect(self.on_combo_box_changed)

        self.ui.pushButton_decrypt.clicked.connect(lambda: self.db_handler.decrypt_data_du(self.ui))

        self.ui.pushButton_keyfile.clicked.connect(lambda: self.db_handler.select_keyfile(self.ui))
        self.ui.pushButton_decryptedfile.clicked.connect(lambda: self.db_handler.select_decryptedfile(self.ui))

    def on_combo_box_changed(self):
        resource_type = self.ui.comboBox_table.currentText()
        access_granted = self.check_access(self.username, resource_type)
        if access_granted:
            self.populate_columns()
    
    def check_access(self, username, resource_type):
        abac = AttributeBasedAccessControl()

        # Lấy thông tin nhân viên từ MySQL
        employee = abac.get_employee_attributes(username)
        print(employee)
        if not employee:
            print(f"No employee found with username {username}")
            return False

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
            return True
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
    
    def on_ok_clicked(self):
        selected_resource = self.ui.cbResource.currentText()  # Đảm bảo truy cập đúng cbResource
        print(f"Selected resource: {selected_resource}")
        # Gọi phương thức kiểm tra truy cập từ fabac.py
        self.check_access(self.username, selected_resource)

    def populate_columns(self):
        # Xóa các widget con của scrollAreaWidgetContents
        while self.ui.verticalLayout_scrollArea.count():
            child = self.ui.verticalLayout_scrollArea.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        table_name = self.ui.comboBox_table.currentText()
        columns = self.db_handler.get_columns(table_name)

        for column in columns:
            checkbox = QCheckBox(column)
            self.ui.verticalLayout_scrollArea.addWidget(checkbox)
