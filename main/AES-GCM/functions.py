import sys
import platform
import subprocess
from PyQt6.QtWidgets import *
from mysql.connector import connect
from aes_gcm import AES_GCM
from gui import Ui_MainWindow

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
