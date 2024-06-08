import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QCheckBox, QVBoxLayout, QSizePolicy
from du_gui import DU_Ui_MainWindow
from PyQt6.QtGui import QIcon
from du_functions import DatabaseHandler

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = DU_Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Data User App")
        #self.setWindowIcon(QIcon('/Users/wanthinnn/Downloads/nekocoffee.icns')) 
        self.db_handler = DatabaseHandler(self.ui)

        self.ui.comboBox_table.addItems(self.db_handler.get_tables())
        self.ui.comboBox_table.currentTextChanged.connect(self.populate_columns)

        self.ui.pushButton_decrypt.clicked.connect(lambda: self.db_handler.decrypt_data_du(self.ui))

        self.ui.pushButton_keyfile.clicked.connect(lambda: self.db_handler.select_keyfile(self.ui))
        self.ui.pushButton_decryptedfile.clicked.connect(lambda: self.db_handler.select_decryptedfile(self.ui))


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




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
