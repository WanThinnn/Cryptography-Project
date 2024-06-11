import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from HOME.home_gui import Home_Ui_MainWindow
from DATA_USER.du_main import AES_MainWindow
from DATA_USER_ABE.du_abe_main import *


class HomeWindows(QMainWindow):
    def __init__(self, username):
        super(HomeWindows, self).__init__()
        self.ui = Home_Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Home: " + username)
        self.username = username
        self.ui.label_2.setText("Hello " + username)
        self.ui.btnAES.clicked.connect(self.open_AES_form)
        self.ui.btnABE.clicked.connect(self.open_ABE_form)
       
    
    def open_AES_form(self):
        self.AES_window = AES_MainWindow(self.username)
        self.AES_window.show()
    
    def open_ABE_form(self):
        self.ABE_window = ABE_MainWindowApp(self.username)
        self.ABE_window.show()

        
    # def open_ABE_form(self):
    #     self.Cloud_window = ABE_MainWindowApp(self.username)
    #     self.Cloud_window.show()


