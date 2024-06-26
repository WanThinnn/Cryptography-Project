import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QCheckBox, QVBoxLayout, QSizePolicy
from DATA_OWNER.do_gui import Ui_MainWindow
from PyQt6.QtGui import QIcon
from DATA_OWNER.do_functions import DatabaseHandler

class AES_MainWindow(QMainWindow):
    def __init__(self, username):
        super(AES_MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("My App: " + username)
        self.setWindowIcon(QIcon('/Users/wanthinnn/Downloads/nekocoffee.icns')) 
        self.db_handler = DatabaseHandler(self.ui)
        self.username = username
        self.ui.comboBox_table.addItems(self.db_handler.get_tables())
        self.ui.comboBox_table.currentTextChanged.connect(self.populate_columns)

        self.ui.pushButton_generate_keys.clicked.connect(lambda: self.db_handler.generate_keys(self.ui))
        self.ui.pushButton_encrypt.clicked.connect(lambda: self.db_handler.encrypt_data(self.ui))
        self.ui.pushButton_decrypt.clicked.connect(lambda: self.db_handler.decrypt_data(self.ui))

        self.ui.pushButton_keyfile.clicked.connect(lambda: self.db_handler.select_keyfile(self.ui))
        self.ui.pushButton_plaintextfile.clicked.connect(lambda: self.db_handler.select_plaintextfile(self.ui))
        self.ui.pushButton_encryptedfile.clicked.connect(lambda: self.db_handler.select_encryptedfile(self.ui))
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




# def Open_AES_form(user):
#     app = QApplication(sys.argv)
#     window = MainWindow(user)
#     window.show()
#     sys.exit(app.exec())
