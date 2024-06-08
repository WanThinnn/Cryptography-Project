import sys
from PyQt6 import QtWidgets
from userGetKeyy import Ui_MainWindow
from functionUser import connect_to_server, disconnect_from_server, select_save_path, perform_setup, config, fetch_key

class MainWindowApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindowApp, self).__init__(parent)
        self.setupUi(self)
        
        # Connect the buttons to their respective functions
        self.getPubPath.clicked.connect(lambda: select_save_path(self, self.pubTxb))
        self.getPriPath.clicked.connect(lambda: select_save_path(self, self.priTxb))
        self.connectBtn.clicked.connect(lambda: connect_to_server(self))
        self.disconnectBtn.clicked.connect(lambda: disconnect_from_server(self))
        self.getPubBtn.clicked.connect(lambda: fetch_key(self, self.pubTxb, "public_key.pem"))
        self.getPriBtn.clicked.connect(lambda: fetch_key(self, self.priTxb, "private_key.pem"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindowApp()
    MainWindow.show()
    sys.exit(app.exec())
