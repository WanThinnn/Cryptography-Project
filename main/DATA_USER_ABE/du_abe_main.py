import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import *
from du_abe_gui import Ui_MainWindow  # Đảm bảo rằng tên file 'userGetKey.ui' đã được biên dịch đúng
from du_abe_functions import ProcessDB

class MainWindowApp(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindowApp, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db_handler = ProcessDB()

        # Populate the table combobox
        self.ui.comboBox_table.addItems(self.db_handler.get_tables())

        # Connect the buttons to their respective functions
        self.ui.getPubPath.clicked.connect(lambda: self.db_handler.select_save_path(self, self.ui.pubTxb))
        self.ui.getPubBtn_2.clicked.connect(lambda: self.db_handler.select_file(self, self.ui.pubTxb))
        self.ui.getPriPath.clicked.connect(lambda: self.db_handler.select_save_path(self, self.ui.priTxb))
        self.ui.getCipPath.clicked.connect(lambda: self.db_handler.select_save_path(self, self.ui.cipTxb))
        self.ui.getRecPath.clicked.connect(lambda: self.db_handler.select_save_path(self, self.ui.recoverTxb))

        self.ui.getPubBtn.clicked.connect(lambda: self.db_handler.fetch_public_key(self.ui, self.ui.pubTxb, "public_key.pem"))
        self.ui.getPriBtn.clicked.connect(lambda: self.db_handler.fetch_private_key(self.ui, self.ui.priTxb, "private_key.pem"))
        self.ui.getCipBtn.clicked.connect(self.handle_get_ciphertext)
        
        self.ui.decryptBtn.clicked.connect(lambda: self.db_handler.decrypt_data(self))
        

    def handle_get_ciphertext(self):
        selected_table = self.ui.comboBox_table.currentText()
        file_path = self.ui.cipTxb.text()
        if selected_table and file_path:
            self.db_handler.get_ciphertext(selected_table, file_path)
            QMessageBox.information(self, "Success", "Data has been written successfully!")
        else:
            QMessageBox.warning(self, "Warning", "Please select a table and specify a file path.")

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
    MainWindow = MainWindowApp()
    MainWindow.show()
    sys.exit(app.exec())
