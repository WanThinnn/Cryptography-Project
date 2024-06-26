# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_LoginWindow(object):
    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(400, 300)
        self.centralwidget = QtWidgets.QWidget(parent=LoginWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_username = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_username.setGeometry(QtCore.QRect(50, 50, 100, 20))
        self.label_username.setObjectName("label_username")
        self.lineEdit_username = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit_username.setGeometry(QtCore.QRect(150, 50, 200, 25))
        self.lineEdit_username.setAutoFillBackground(True)
        self.lineEdit_username.setObjectName("lineEdit_username")
        self.label_password = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_password.setGeometry(QtCore.QRect(50, 100, 100, 20))
        self.label_password.setObjectName("label_password")
        self.lineEdit_password = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit_password.setGeometry(QtCore.QRect(150, 100, 200, 25))
        self.lineEdit_password.setAutoFillBackground(True)
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.pushButton_login = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_login.setGeometry(QtCore.QRect(150, 150, 100, 31))
        self.pushButton_login.setStyleSheet("color: rgb(255, 255, 255);\n"
"    background-color: rgb(26, 95, 180);")
        self.pushButton_login.setObjectName("pushButton_login")
        self.pushButton_signup = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_signup.setGeometry(QtCore.QRect(150, 210, 100, 30))
        self.pushButton_signup.setStyleSheet("color: rgb(255, 255, 255);\n"
"    background-color: rgb(26, 95, 180);")
        self.pushButton_signup.setObjectName("pushButton_signup")
        LoginWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=LoginWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 22))
        self.menubar.setObjectName("menubar")
        LoginWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=LoginWindow)
        self.statusbar.setObjectName("statusbar")
        LoginWindow.setStatusBar(self.statusbar)

        self.retranslateUi(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)

    def retranslateUi(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        LoginWindow.setWindowTitle(_translate("LoginWindow", "Login"))
        self.label_username.setText(_translate("LoginWindow", "Username:"))
        self.label_password.setText(_translate("LoginWindow", "Password:"))
        self.pushButton_login.setText(_translate("LoginWindow", "Login"))
        self.pushButton_signup.setText(_translate("LoginWindow", "Sign Up"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LoginWindow = QtWidgets.QMainWindow()
    ui = Ui_LoginWindow()
    ui.setupUi(LoginWindow)
    LoginWindow.show()
    sys.exit(app.exec())
