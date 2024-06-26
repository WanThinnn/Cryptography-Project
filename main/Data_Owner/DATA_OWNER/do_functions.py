import sys
import os
# Lấy đường dẫn hiện tại của tệp đang chạy
current_dir = os.path.dirname(os.path.abspath(__file__))

# Lấy đường dẫn của thư mục cha
parent_dir = os.path.dirname(current_dir)
from PyQt6.QtWidgets import *
# Thêm đường dẫn của thư mục cha vào sys.path
sys.path.append(parent_dir)
import platform
import subprocess
from PyQt6.QtWidgets import *
from mysql.connector import connect
aes_gcm_dir = os.path.join(parent_dir, 'AES_GCM')
sys.path.append(aes_gcm_dir)
from AES_GCM.aes_gcm import *

# from cloud import *

class DatabaseHandler:
    def __init__(self, ui):
        self.connection = connect(
            host="company-database.clce6ae44hhz.ap-southeast-2.rds.amazonaws.com",
            user="admin",
            password="24122003",
            database="company_db"
        )
        self.aes_gcm = AES_GCM()
        self.ui = ui
        # self.process_cloud = ProcessCloud()  # Instance of ProcessCloud
        self.keyfile = ''
        self.plaintext_file = ''
        self.encrypted_file = ''
        self.decrypted_file = ''

        self.os_type = platform.system()

    def get_tables(self):
        query = "SHOW TABLES"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return [row[0] for row in result]

    def get_columns(self, table_name):
        query = f"SHOW COLUMNS FROM {table_name}"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return [row[0] for row in result]

    def get_selected_columns(self):
        return [self.ui.verticalLayout_scrollArea.itemAt(i).widget().text() for i in range(self.ui.verticalLayout_scrollArea.count()) if self.ui.verticalLayout_scrollArea.itemAt(i).widget().isChecked()]

    def select_keyfile(self, ui):
        keyfile, _ = QFileDialog.getOpenFileName(None, "Select Key File", "", "All Files (*)")
        if keyfile:
            ui.lineEdit_keyfile.setText(keyfile)
            self.keyfile = keyfile


    def select_plaintextfile(self, ui):
        plaintext_file, _ = QFileDialog.getOpenFileName(None, "Select Plaintext File", "", "CSV Files (*.csv);;All Files (*)")
        if plaintext_file:
            ui.lineEdit_plaintextfile.setText(plaintext_file)
            self.plaintext_file = plaintext_file

    def select_encryptedfile(self, ui):
        encrypted_file, _ = QFileDialog.getOpenFileName(None, "Select Encrypted File", "", "CSV Files (*.csv);;All Files (*)")
        if encrypted_file:
            ui.lineEdit_encryptedfile.setText(encrypted_file)
            self.encrypted_file = encrypted_file

    def select_decryptedfile(self, ui):
        decrypted_file, _ = QFileDialog.getOpenFileName(None, "Select Decrypted File", "", "CSV Files (*.csv);;All Files (*)")
        if decrypted_file:
            ui.lineEdit_decryptedfile.setText(decrypted_file)
            self.decrypted_file = decrypted_file

    # def show_message(self, title, message):
    #     if self.os_type == 'Darwin':  # macOS
    #         script = f'display notification "{message}" with title "{title}"'
    #         subprocess.run(['osascript', '-e', script])
    #     elif self.os_type == 'Linux':  # Ubuntu
    #         subprocess.run(['zenity', '--info', '--title', title, '--text', message])
    
    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()


    def generate_keys(self, ui):
        selected_columns = self.get_selected_columns()
        if not self.keyfile:
            self.select_keyfile(ui)
        if self.keyfile:
            self.aes_gcm.gen_key(selected_columns, self.keyfile)

            self.show_message("Success", "Keys and IVs have been generated successfully.")

    def encrypt_data(self, ui):
        selected_columns = self.get_selected_columns()

        if not self.plaintext_file:
            self.select_plaintextfile(ui)
        if not self.encrypted_file:
            self.select_encryptedfile(ui)
        if not self.keyfile:
            self.select_keyfile(ui)
    
        if self.plaintext_file and self.keyfile:
            self.aes_gcm.encrypt_data(self.encrypted_file, selected_columns, None, self.plaintext_file, self.keyfile)
            self.show_message("Success", "Data has been encrypted successfully.")

    def decrypt_data(self, ui):
        selected_columns = self.get_selected_columns()

        if not self.encrypted_file:
            self.select_encryptedfile(ui)
        if not self.decrypted_file:
            self.select_decryptedfile(ui)
        if not self.keyfile:
            self.select_keyfile(ui)


        if self.encrypted_file and self.keyfile:
            self.aes_gcm.decrypt_data(self.decrypted_file, selected_columns, None, self.encrypted_file, self.keyfile)
            self.show_message("Success", "Data has been decrypted successfully.")
    
    def decrypt_data_du(self, ui):
        selected_columns = self.get_selected_columns()

        if not self.encrypted_file:
            # Truy vấn cơ sở dữ liệu và lưu dữ liệu vào file CSV
            query = "SELECT * FROM your_table_name"  # Thay thế bằng câu truy vấn của bạn
            self.encrypted_file = self.process_cloud.query_db_to_csv(query, "temporary_encrypted_file.csv")

        if not self.decrypted_file:
            self.select_decryptedfile(ui)
        if not self.keyfile:
            self.select_keyfile(ui)

        if self.encrypted_file and self.keyfile:
            self.aes_gcm.decrypt_data(self.decrypted_file, selected_columns, None, self.encrypted_file, self.keyfile)
            self.show_message("Success", "Data has been decrypted successfully.")

