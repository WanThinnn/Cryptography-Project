import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox, QCheckBox
from DATA_USER_ABE.du_abe_gui import Ui_MainWindow  # Đảm bảo rằng tên file 'userGetKey.ui' đã được biên dịch đúng
from DATA_USER_ABE.du_abe_functions import ProcessDB
from ABAC.classABAC import AttributeBasedAccessControl

class ABE_MainWindowApp(QtWidgets.QMainWindow):
    def __init__(self, username, parent=None):
        super(ABE_MainWindowApp, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db_handler = ProcessDB()
        self.username = username
        # Populate the table combobox
        self.ui.comboBox_table.addItems(self.db_handler.get_tables())
        self.ui.comboBox_table.currentTextChanged.connect(self.on_combo_box_changed)

        # Connect the buttons to their respective functions
        self.ui.getPubPath.clicked.connect(lambda: self.db_handler.select_save_path(self, self.ui.pubTxb))
        self.ui.getPubBtn_2.clicked.connect(lambda: self.db_handler.select_file(self, self.ui.pubTxb))
        self.ui.getPriPath.clicked.connect(lambda: self.db_handler.select_save_path(self, self.ui.priTxb))
        self.ui.getCipPath.clicked.connect(lambda: self.db_handler.select_save_path(self, self.ui.cipTxb))
        self.ui.getRecPath.clicked.connect(lambda: self.db_handler.select_save_path(self, self.ui.recoverTxb))

        self.ui.getPubBtn.clicked.connect(lambda: self.db_handler.fetch_public_key(self.ui, self.ui.pubTxb, "public_key.bin", "127.0.0.1", 10023))
        self.ui.getPriBtn.clicked.connect(lambda: self.db_handler.fetch_private_key(self.ui, self.username, self.ui.priTxb, "private_key.bin", "127.0.0.1", 10023))
        self.ui.getCipBtn.clicked.connect(self.handle_get_ciphertext)
        
        self.ui.decryptBtn.clicked.connect(lambda: self.db_handler.decrypt_data(self))

    def on_combo_box_changed(self):
        self.check_access(self.username, self.ui.comboBox_table.currentText())
        self.populate_columns()

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
        
    def handle_get_ciphertext(self):
        selected_table = self.ui.comboBox_table.currentText()
        file_path = self.ui.cipTxb.text()
        if selected_table and file_path:
            self.db_handler.get_ciphertext(selected_table, file_path)
            QMessageBox.information(self, "Success", "Data has been written successfully!")
        else:
            QMessageBox.warning(self, "Warning", "Please select a table and specify a file path.")

    def populate_columns(self):
        # # Xóa các widget con của scrollAreaWidgetContents
        # while self.ui.verticalLayout_scrollArea.count():
        #     child = self.ui.verticalLayout_scrollArea.takeAt(0)
        #     if child.widget():
        #         child.widget().deleteLater()

        # table_name = self.ui.comboBox_table.currentText()
        # columns = self.db_handler.get_columns(table_name)

        # for column in columns:
        #     checkbox = QCheckBox(column)
        #     self.ui.verticalLayout_scrollArea.addWidget(checkbox)
        pass

    def update_table_combobox(self):
        current_table = self.ui.comboBox_table.currentText()
        tables = self.db_handler.get_tables()

        if tables:
            self.ui.comboBox_table.clear()
            self.ui.comboBox_table.addItems(tables)

            # Kiểm tra xem bảng hiện tại có trong danh sách bảng mới hay không
            if current_table in tables:
                self.ui.comboBox_table.setCurrentText(current_table)
            else:
                self.ui.comboBox_table.setCurrentIndex(0)
        else:
            self.ui.comboBox_table.clear()
            QMessageBox.warning(self, "Warning", "No tables found in the database.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = ABE_MainWindowApp("username")
    MainWindow.show()
    sys.exit(app.exec())
