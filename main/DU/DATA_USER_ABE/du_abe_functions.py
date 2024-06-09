import subprocess
from PyQt6 import QtWidgets
from DATA_USER_ABE.client import Client
from PyQt6.QtWidgets import *
import mysql.connector
from DATA_USER_ABE.f_cpabe import *

class Config:
    def __init__(self):
        self.server_process = None
        self.selected_path = None


config = Config()


class ProcessDB:
    def __init__(self):
        self.host = "company-database.clce6ae44hhz.ap-southeast-2.rds.amazonaws.com"
        self.user = "admin"
        self.password = "24122003"
        self.database = "company_db"
        self.connection = self.connect_to_db()
        self.plaintext_file = None
        self.encrypted_file = None
        self.decrypted_file = None
        self.keyfile = None

    def connect_to_db(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def get_ciphertext(self, table_name, file_path):
        cursor = self.connection.cursor()
        cipher_file = file_path + '/' + table_name + '.csv'
        try:
            query = f"SELECT * FROM {table_name}"
            cursor.execute(query)
            result = cursor.fetchall()

            # Get the column names
            columns = [desc[0] for desc in cursor.description]

            # Write the column names to the file
            with open(cipher_file, 'w') as file:
                file.write(','.join(columns) + '\n')

                # Write the data to the file
                for row in result:
                    file.write(','.join(map(str, row)) + '\n')

            print(f"Data has been written to {file_path}")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()


    def get_tables(self):
        cursor = self.connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        cursor.close()
        return tables

    def connect_to_server(self, ui):
        try:
            if config.server_process is None:
                # Start the server process
                config.server_process = subprocess.Popen(['python3', 'server.py'])
                QtWidgets.QMessageBox.information(ui.centralwidget, 'Thông báo', 'Máy chủ đã được khởi động thành công!')
            else:
                QtWidgets.QMessageBox.warning(ui.centralwidget, 'Cảnh báo', 'Máy chủ đã đang chạy!')
        except Exception as e:
            QtWidgets.QMessageBox.critical(ui.centralwidget, 'Lỗi', f'Không thể khởi động máy chủ: {e}')

    def disconnect_from_server(self, ui):
        try:
            if config.server_process:
                config.server_process.terminate()
                config.server_process = None
                QtWidgets.QMessageBox.information(ui.centralwidget, 'Thông báo', 'Máy chủ đã được tắt!')
            else:
                QtWidgets.QMessageBox.warning(ui.centralwidget, 'Cảnh báo', 'Không có máy chủ nào đang chạy!')
        except Exception as e:
            QtWidgets.QMessageBox.critical(ui.centralwidget, 'Lỗi', f'Không thể tắt máy chủ: {e}')

    def select_save_path(self, parent, lineedit):
        dialog = QtWidgets.QFileDialog()
        path = dialog.getExistingDirectory(parent, 'Chọn thư mục lưu trữ')
        if path:
            lineedit.setText(path)
            # QtWidgets.QMessageBox.information(parent, 'Thông báo', f'Đường dẫn đã chọn: {path}')
    def select_file(self, parent, lineedit):
        dialog = QtWidgets.QFileDialog()
        path, _ = dialog.getOpenFileName(parent, 'Chọn file')
        if path:
            lineedit.setText(path)
            # QtWidgets.QMessageBox.information(parent, 'Thông báo', f'Đường dẫn đã chọn: {path}')


    def perform_setup(self, ui):
        if not config.selected_path:
            QtWidgets.QMessageBox.warning(ui.centralwidget, 'Cảnh báo', 'Vui lòng chọn đường dẫn lưu trữ trước!')
            return

        server_ip = ui.ipInput.text()
        server_port = int(ui.portInput.text())
        file_name = "public_key.pem"  # Fixed file name

        client = Client(host=server_ip, port=server_port)
        client.connect_to_server('setup', None, config.selected_path, file_name)
        QtWidgets.QMessageBox.information(ui.centralwidget, 'Thông báo', 'Setup completed và file đã được lưu!')
        
    def get_cip_path(self, ui):
        dialog = QtWidgets.QFileDialog()
        path = dialog.getExistingDirectory(self, 'Chọn thư mục lưu trữ')
        if path:
            ui.cipTxb.setText(path)
            QtWidgets.QMessageBox.information(self, 'Thông báo', f'Đường dẫn đã chọn: {path}')
            
    def fetch_private_key(self, ui, username, lineedit, file_name):
        save_path = lineedit.text()
        if not save_path:
            # Debugging print to check the type and value of ui.centralwidget
            print(f"ui.centralwidget: {ui.centralwidget}, type: {type(ui.centralwidget)}")
            if not isinstance(ui.centralwidget, QtWidgets.QWidget):
                raise TypeError(f"ui.centralwidget is not of type QWidget or not assigned correctly: {type(ui.centralwidget)}")
            QtWidgets.QMessageBox.warning(ui.centralwidget, 'Cảnh báo', 'Vui lòng chọn đường dẫn lưu trữ trước!')
            return

        server_ip = "192.168.1.4"
        server_port = 10023

        client = Client(host=server_ip, port=server_port)
        client.connect_to_server('genkey', username=username, save_path=save_path, file_name=file_name)
        QtWidgets.QMessageBox.information(ui.centralwidget, 'Thông báo', f'{file_name} đã được lưu tại {save_path}!')

    def fetch_public_key(self, ui, lineedit, file_name):
        save_path = lineedit.text()
        if not save_path:
            # Debugging print to check the type and value of ui.centralwidget
            print(f"ui.centralwidget: {ui.centralwidget}, type: {type(ui.centralwidget)}")
            if not isinstance(ui.centralwidget, QtWidgets.QWidget):
                raise TypeError(f"ui.centralwidget is not of type QWidget or not assigned correctly: {type(ui.centralwidget)}")
            QtWidgets.QMessageBox.warning(ui.centralwidget, 'Cảnh báo', 'Vui lòng chọn đường dẫn lưu trữ trước!')
            return

        server_ip = "192.168.1.4"
        server_port = 10023

        client = Client(host=server_ip, port=server_port)
        client.connect_to_server('get_pub_key', None, save_path, file_name)
        QtWidgets.QMessageBox.information(ui.centralwidget, 'Thông báo', f'{file_name} đã được lưu tại {save_path}!')
    
    def decrypt_data(self, parent):
        table = parent.ui.comboBox_table.currentText()
        public_key_path = parent.ui.pubTxb.text()
        if not public_key_path.endswith('/public_key.pem'):
            public_key_path += '/public_key.pem'
        private_key_path = parent.ui.priTxb.text() + '/private_key.pem'
        recover_file = parent.ui.recoverTxb.text() + f'/key_{table}_aes.csv'
        ciphertext_file = parent.ui.cipTxb.text() + f'/{table}.csv'
        if not public_key_path or not recover_file or not private_key_path or not ciphertext_file:
            QMessageBox.warning(parent, "Warning", "Please ensure all paths are selected.")
            return

        try:
            print(f"Starting encryption with public_key_path: {public_key_path}, plaintext_path: {recover_file}")

            cpabe = CPABE("AC17")
            decrypt_message(cpabe, public_key_path, private_key_path, ciphertext_file, recover_file)
            QMessageBox.information(parent, "Success", "Data Decrypted and saved successfully.")

        except Exception as e:
            QMessageBox.critical(parent, "Error", f"Decryption failed: {str(e)}")
            print(f"Encryption failed: {str(e)}")
