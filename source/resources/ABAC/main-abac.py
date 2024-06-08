from PyQt6 import QtWidgets
from abac import Ui_MainWindow
# from fabac import các_hàm_xử_lí_nếu_có

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Kết nối các sự kiện và hàm xử lí nếu cần

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec())
