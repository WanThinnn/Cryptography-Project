# Form implementation generated from reading ui file 'du_gui.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class DU_Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(589, 515)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit_keyfile = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit_keyfile.setGeometry(QtCore.QRect(180, 280, 371, 31))
        self.lineEdit_keyfile.setObjectName("lineEdit_keyfile")
        self.pushButton_decrypt = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_decrypt.setGeometry(QtCore.QRect(230, 400, 141, 51))
        self.pushButton_decrypt.setStyleSheet("background-color: rgb(53, 132, 228);\n"
"color: rgb(255, 255, 255);")
        self.pushButton_decrypt.setObjectName("pushButton_decrypt")
        self.pushButton_keyfile = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_keyfile.setGeometry(QtCore.QRect(40, 280, 131, 35))
        self.pushButton_keyfile.setStyleSheet("background-color: rgb(153, 193, 241);")
        self.pushButton_keyfile.setObjectName("pushButton_keyfile")
        self.pushButton_decryptedfile = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_decryptedfile.setGeometry(QtCore.QRect(40, 330, 131, 31))
        self.pushButton_decryptedfile.setStyleSheet("background-color: rgb(153, 193, 241);")
        self.pushButton_decryptedfile.setObjectName("pushButton_decryptedfile")
        self.comboBox_table = QtWidgets.QComboBox(parent=self.centralwidget)
        self.comboBox_table.setGeometry(QtCore.QRect(40, 40, 511, 41))
        self.comboBox_table.setObjectName("comboBox_table")
        self.lineEdit_decryptedfile = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit_decryptedfile.setGeometry(QtCore.QRect(180, 330, 371, 31))
        self.lineEdit_decryptedfile.setObjectName("lineEdit_decryptedfile")
        self.scrollArea = QtWidgets.QScrollArea(parent=self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(45, 90, 501, 171))
        self.scrollArea.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 499, 169))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_scrollArea = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_scrollArea.setObjectName("verticalLayout_scrollArea")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 589, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_decrypt.setText(_translate("MainWindow", "Decrypt"))
        self.pushButton_keyfile.setText(_translate("MainWindow", "Key File"))
        self.pushButton_decryptedfile.setText(_translate("MainWindow", "Decrypted File"))
