from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(617, 401)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lbUsername = QtWidgets.QLabel(parent=self.centralwidget)
        self.lbUsername.setGeometry(QtCore.QRect(30, 30, 67, 17))
        self.lbUsername.setObjectName("lbUsername")
        self.cbResource = QtWidgets.QComboBox(parent=self.centralwidget)
        self.cbResource.setGeometry(QtCore.QRect(150, 70, 241, 25))
        self.cbResource.setObjectName("cbResource")
        self.cbResource.addItem("")
        self.cbResource.addItem("")
        self.cbResource.addItem("")
        self.cbResource.addItem("")
        self.btnOK = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnOK.setGeometry(QtCore.QRect(390, 70, 51, 25))
        self.btnOK.setObjectName("btnOK")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 617, 22))
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
        self.lbUsername.setText(_translate("MainWindow", "Welcome "))
        self.cbResource.setItemText(0, _translate("MainWindow", "Meeting Report"))
        self.cbResource.setItemText(1, _translate("MainWindow", "Basic Documents"))
        self.cbResource.setItemText(2, _translate("MainWindow", "Internal Documents"))
        self.cbResource.setItemText(3, _translate("MainWindow", "ExecutiveDocuments"))
        self.btnOK.setText(_translate("MainWindow", "OK"))
