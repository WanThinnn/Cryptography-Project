# Form implementation generated from reading ui file 'du_abe_gui.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(815, 467)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.homeBtn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.homeBtn.setGeometry(QtCore.QRect(20, 10, 111, 41))
        self.homeBtn.setStyleSheet("color: rgb(255, 255, 255);\n"
"    background-color: rgb(26, 95, 180);")
        self.homeBtn.setObjectName("homeBtn")
        self.getPriBtn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.getPriBtn.setGeometry(QtCore.QRect(530, 230, 131, 31))
        self.getPriBtn.setStyleSheet("color: rgb(255, 255, 255);\n"
"    background-color: rgb(26, 95, 180);")
        self.getPriBtn.setObjectName("getPriBtn")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 180, 131, 31))
        self.label.setObjectName("label")
        self.getCipBtn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.getCipBtn.setGeometry(QtCore.QRect(530, 280, 131, 31))
        self.getCipBtn.setStyleSheet("color: rgb(255, 255, 255);\n"
"    background-color: rgb(26, 95, 180);")
        self.getCipBtn.setObjectName("getCipBtn")
        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 230, 131, 31))
        self.label_2.setObjectName("label_2")
        self.getPubBtn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.getPubBtn.setGeometry(QtCore.QRect(530, 130, 131, 31))
        self.getPubBtn.setStyleSheet("color: rgb(255, 255, 255);\n"
"    background-color: rgb(26, 95, 180);")
        self.getPubBtn.setObjectName("getPubBtn")
        self.label_3 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 130, 131, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 280, 131, 31))
        self.label_4.setObjectName("label_4")
        self.getPubPath = QtWidgets.QPushButton(parent=self.centralwidget)
        self.getPubPath.setGeometry(QtCore.QRect(430, 130, 71, 31))
        self.getPubPath.setStyleSheet("background-color: rgb(153, 193, 241);")
        self.getPubPath.setObjectName("getPubPath")
        self.getPriPath = QtWidgets.QPushButton(parent=self.centralwidget)
        self.getPriPath.setGeometry(QtCore.QRect(430, 180, 71, 31))
        self.getPriPath.setStyleSheet("background-color: rgb(153, 193, 241);")
        self.getPriPath.setObjectName("getPriPath")
        self.getCipPath = QtWidgets.QPushButton(parent=self.centralwidget)
        self.getCipPath.setGeometry(QtCore.QRect(430, 230, 71, 31))
        self.getCipPath.setStyleSheet("background-color: rgb(153, 193, 241);")
        self.getCipPath.setObjectName("getCipPath")
        self.getRecPath = QtWidgets.QPushButton(parent=self.centralwidget)
        self.getRecPath.setGeometry(QtCore.QRect(430, 280, 71, 31))
        self.getRecPath.setStyleSheet("background-color: rgb(153, 193, 241);")
        self.getRecPath.setObjectName("getRecPath")
        self.comboBox_table = QtWidgets.QComboBox(parent=self.centralwidget)
        self.comboBox_table.setGeometry(QtCore.QRect(160, 60, 411, 51))
        self.comboBox_table.setObjectName("comboBox_table")
        self.decryptBtn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.decryptBtn.setGeometry(QtCore.QRect(340, 350, 161, 61))
        self.decryptBtn.setStyleSheet("color: rgb(255, 255, 255);\n"
"    background-color: rgb(26, 95, 180);")
        self.decryptBtn.setObjectName("decryptBtn")
        self.getTableBtn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.getTableBtn.setGeometry(QtCore.QRect(570, 60, 101, 51))
        self.getTableBtn.setStyleSheet("background-color: rgb(153, 193, 241);")
        self.getTableBtn.setObjectName("getTableBtn")
        self.getPubBtn_2 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.getPubBtn_2.setGeometry(QtCore.QRect(530, 180, 131, 31))
        self.getPubBtn_2.setStyleSheet("background-color: rgb(153, 193, 241);")
        self.getPubBtn_2.setObjectName("getPubBtn_2")
        self.pubTxb = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.pubTxb.setGeometry(QtCore.QRect(160, 130, 271, 31))
        self.pubTxb.setObjectName("pubTxb")
        self.priTxb = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.priTxb.setGeometry(QtCore.QRect(160, 180, 271, 31))
        self.priTxb.setObjectName("priTxb")
        self.cipTxb = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.cipTxb.setGeometry(QtCore.QRect(160, 230, 271, 31))
        self.cipTxb.setObjectName("cipTxb")
        self.recoverTxb = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.recoverTxb.setGeometry(QtCore.QRect(160, 280, 271, 31))
        self.recoverTxb.setObjectName("recoverTxb")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 815, 22))
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
        self.homeBtn.setText(_translate("MainWindow", "Home"))
        self.getPriBtn.setText(_translate("MainWindow", "Get Private Key"))
        self.label.setText(_translate("MainWindow", "Private_key path"))
        self.getCipBtn.setText(_translate("MainWindow", "Get Cipher Text"))
        self.label_2.setText(_translate("MainWindow", "Cipher_text path"))
        self.getPubBtn.setText(_translate("MainWindow", "Get Public Key"))
        self.label_3.setText(_translate("MainWindow", "Public_key path"))
        self.label_4.setText(_translate("MainWindow", "Recover_text path"))
        self.getPubPath.setText(_translate("MainWindow", "Choose"))
        self.getPriPath.setText(_translate("MainWindow", "Choose"))
        self.getCipPath.setText(_translate("MainWindow", "Choose"))
        self.getRecPath.setText(_translate("MainWindow", "Choose"))
        self.decryptBtn.setText(_translate("MainWindow", "Decrypt"))
        self.getTableBtn.setText(_translate("MainWindow", "Choose"))
        self.getPubBtn_2.setText(_translate("MainWindow", "Choose Public Key"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
