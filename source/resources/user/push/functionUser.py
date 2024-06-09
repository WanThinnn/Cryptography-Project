import subprocess
import os
from PyQt6 import QtWidgets
from client import Client

# Configuration
class Config:
    def __init__(self):
        self.server_process = None
        self.selected_path = None

config = Config()

def connect_to_server(ui):
    try:
        if config.server_process is None:
            # Start the server process
            config.server_process = subprocess.Popen(['python3', 'server.py'])
            QtWidgets.QMessageBox.information(ui.centralwidget, 'Thông báo', 'Máy chủ đã được khởi động thành công!')
        else:
            QtWidgets.QMessageBox.warning(ui.centralwidget, 'Cảnh báo', 'Máy chủ đã đang chạy!')
    except Exception as e:
        QtWidgets.QMessageBox.critical(ui.centralwidget, 'Lỗi', f'Không thể khởi động máy chủ: {e}')

def disconnect_from_server(ui):
    try:
        if config.server_process:
            config.server_process.terminate()
            config.server_process = None
            QtWidgets.QMessageBox.information(ui.centralwidget, 'Thông báo', 'Máy chủ đã được tắt!')
        else:
            QtWidgets.QMessageBox.warning(ui.centralwidget, 'Cảnh báo', 'Không có máy chủ nào đang chạy!')
    except Exception as e:
        QtWidgets.QMessageBox.critical(ui.centralwidget, 'Lỗi', f'Không thể tắt máy chủ: {e}')

def select_save_path(ui, textbox):
    dialog = QtWidgets.QFileDialog()
    path = dialog.getExistingDirectory(ui.centralwidget, 'Chọn thư mục lưu trữ')
    if path:
        textbox.setPlainText(path)
        QtWidgets.QMessageBox.information(ui.centralwidget, 'Thông báo', f'Đường dẫn đã chọn: {path}')

def perform_setup(ui):
    if not config.selected_path:
        QtWidgets.QMessageBox.warning(ui.centralwidget, 'Cảnh báo', 'Vui lòng chọn đường dẫn lưu trữ trước!')
        return

    server_ip = ui.ipInput.text()
    server_port = int(ui.portInput.text())
    file_name = "public_key.pem"  # Fixed file name

    client = Client(host=server_ip, port=server_port)
    client.connect_to_server('setup', None, config.selected_path, file_name)
    QtWidgets.QMessageBox.information(ui.centralwidget, 'Thông báo', 'Setup completed và file đã được lưu!')

def fetch_key(ui, textbox, file_name):
    save_path = textbox.toPlainText()
    if not save_path:
        QtWidgets.QMessageBox.warning(ui.centralwidget, 'Cảnh báo', 'Vui lòng chọn đường dẫn lưu trữ trước!')
        return

    server_ip = ui.ipInput.text()
    server_port = int(ui.portInput.text())

    client = Client(host=server_ip, port=server_port)
    client.connect_to_server('genkey', None, save_path, file_name)
    QtWidgets.QMessageBox.information(ui.centralwidget, 'Thông báo', f'{file_name} đã được lưu tại {save_path}!')
