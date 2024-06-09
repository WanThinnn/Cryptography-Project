import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QTableWidgetItem,QMessageBox
from PyQt6.QtGui import QIcon
from IMPORT_CLOUD.do_import_gui import Cloud_Ui_MainWindow
from IMPORT_CLOUD.do_import_cloud import ProcessCloud

class Cloud_MainWindow(QMainWindow):
    def __init__(self, username):
        super(Cloud_MainWindow, self).__init__()
        self.ui = Cloud_Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("My App: " + username)
        self.setWindowIcon(QIcon('/Users/wanthinnn/Downloads/nekocoffee.icns'))
        self.db_handler = ProcessCloud()

        self.ui.comboBox_table.addItems(self.db_handler.get_tables())
        self.ui.comboBox_table.currentTextChanged.connect(self.populate_table_view)
        self.ui.pushButton_import.clicked.connect(self.import_data)
        self.ui.pushButton_plaintextfile.clicked.connect(lambda: self.db_handler.select_plaintextfile(self))
        self.ui.pushButton_Refresh.clicked.connect(self.refresh_tables)

    def import_data(self):
        self.db_handler.import_data(self.ui)

    def refresh_tables(self):
        self.connection = self.db_handler.deconnect_from_db()
        self.populate_table_view()

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

    def populate_table_view(self):
        table_name = self.ui.comboBox_table.currentText()
        if table_name:
            data, columns = self.db_handler.get_table_data(table_name)

            # Clear old data
            self.ui.tableWidget.setRowCount(0)
            self.ui.tableWidget.setColumnCount(0)

            if data:
                self.ui.tableWidget.setColumnCount(len(columns))
                self.ui.tableWidget.setHorizontalHeaderLabels(columns)
                
                for row_number, row_data in enumerate(data):
                    self.ui.tableWidget.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.ui.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        else:
            QMessageBox.warning(self, "Warning", "Please select a table.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
