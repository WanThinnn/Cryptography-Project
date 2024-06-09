import sys
from PyQt6 import QtWidgets
from DO_ABE_GUI import Ui_MainWindow
from DO_ABE import *

class MainWindowApp(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindowApp, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.handler = doCPABE()

        # Connect the buttons to their respective functions
        self.ui.getPubPath.clicked.connect(lambda: self.handler.select_save_path(self, self.ui.pubPathTxb))
        self.ui.getPubBtn.clicked.connect(lambda: self.handler.fetch_key(self, self.ui.pubPathTxb, "public_key.bin", "127.0.0.1", 10023))
        self.ui.uploadPubBtn.clicked.connect(lambda: self.handler.select_save_path(self, self.ui.pubFileTxb, is_file=True))
        self.ui.uploadCipBtn.clicked.connect(lambda: self.handler.select_save_path(self, self.ui.cipTxb, is_file=True))
        self.ui.uploadPlaintBtn.clicked.connect(lambda: self.handler.select_save_path(self, self.ui.plaTxb, is_file=True))
        self.ui.encryptBtn.clicked.connect(lambda: self.handler.encrypt_data(self))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindowApp()
    MainWindow.show()
    sys.exit(app.exec())
