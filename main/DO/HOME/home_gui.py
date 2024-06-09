from PyQt6 import QtCore, QtGui, QtWidgets

class Home_Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(602, 312)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.btnAES = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnAES.setGeometry(QtCore.QRect(310, 110, 151, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnAES.setFont(font)
        self.btnAES.setStyleSheet("background-color: rgb(53, 132, 228);\n"
"color: rgb(255, 255, 255); font-size: 16px; font-weight: bold;")
        self.btnAES.setObjectName("btnAES")

        self.btnABE = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnABE.setGeometry(QtCore.QRect(120, 110, 161, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnABE.setFont(font)
        self.btnABE.setStyleSheet("background-color: rgb(53, 132, 228);\n"
"color: rgb(255, 255, 255); font-size: 16px; font-weight: bold;")
        self.btnABE.setObjectName("btnABE")

        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(250, 50, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(36)  # Increase font size
        font.setBold(True)
        font.setWeight(99)  # Set maximum font weight
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 191, 16))
        font = QtGui.QFont()
        font.setPointSize(20)  # Increase font size
        font.setBold(True)
        font.setWeight(99)  # Set maximum font weight
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.btnCloud = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnCloud.setGeometry(QtCore.QRect(210, 180, 161, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnCloud.setFont(font)
        self.btnCloud.setStyleSheet("background-color: rgb(53, 132, 228);\n"
"color: rgb(255, 255, 255); font-size: 16px; font-weight: bold;")
        self.btnCloud.setObjectName("btnCloud")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 602, 22))
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
        self.btnAES.setText(_translate("MainWindow", "AES Decryption"))
        self.btnABE.setText(_translate("MainWindow", "CP-ABE Decryption"))
        self.label.setText(_translate("MainWindow", "HOME"))
        self.label_2.setText(_translate("MainWindow", "Hello"))
        self.btnCloud.setText(_translate("MainWindow", "Upload to Cloud"))
