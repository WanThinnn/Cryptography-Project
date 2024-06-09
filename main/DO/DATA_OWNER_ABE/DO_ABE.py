from PyQt6.QtWidgets import QFileDialog, QMessageBox
import os
from DATA_OWNER_ABE.client import *
from DATA_OWNER_ABE.f_cpabe import *
from DATA_OWNER_ABE.CPABE import *
from DATA_OWNER_ABE.SerializeCTXT import *

class doCPABE:
    def __init__(self):
        self.plaintext_file = None
        self.encrypted_file = None
        self.decrypted_file = None
        self.keyfile = None

    def select_save_path(self, ui, text_browser, is_file=False):
        if is_file:
            file_path, _ = QFileDialog.getOpenFileName(ui, "Select File")
            if file_path:
                text_browser.setText(file_path)
        else:
            directory = QFileDialog.getExistingDirectory(ui, "Select Directory")
            if directory:
                text_browser.setText(directory)

    def fetch_key(self, ui, text_browser, file_name, Server_ip, Server_port):
        save_path = text_browser.toPlainText()
        if not save_path:
            QMessageBox.warning(ui, "Warning", "Please select a save path first.")
            return

        server_ip = Server_ip
        server_port = Server_port
        if not server_ip or not server_port:
            QMessageBox.warning(ui, "Warning", "Please provide the server IP and port.")
            return

        try:
            server_port = int(server_port)
        except ValueError:
            QMessageBox.warning(ui, "Warning", "Port must be an integer.")
            return

        client = Client(host=server_ip, port=server_port)
        try:
            client.connect_to_server('get_pub_key',save_path=save_path, file_name=file_name)
            QMessageBox.information(ui, "Success", "Public key fetched successfully.")
        except Exception as e:
            QMessageBox.critical(ui, "Error", f"Failed to fetch public key: {str(e)}")

    def encrypt_data(self, parent):
        public_key_path = parent.ui.pubFileTxb.toPlainText()
        plaintext_path = parent.ui.plaTxb.toPlainText()
        ciphertext_file = parent.ui.cipTxb.toPlainText()
        if not public_key_path or not plaintext_path:
            QMessageBox.warning(parent, "Warning", "Please ensure all paths are selected.")
            return

        try:
            print(f"Starting encryption with public_key_path: {public_key_path}, plaintext_path: {plaintext_path}")

            # # Prompt user to select save location for ciphertext
            # options = QFileDialog.Option()
            # save_path, _ = QFileDialog.getSaveFileName(parent, "Save Ciphertext", "", "CSV Files (*.csv);;All Files (*)", options=options)
            # if not save_path:
            #     QMessageBox.warning(parent, "Warning", "Save path was not selected.")
            #     return

            cpabe = CPABE("AC17")
            encrypt_message(cpabe, public_key_path, plaintext_path, ciphertext_file)
            QMessageBox.information(parent, "Success", "Data encrypted and saved successfully.")

        except Exception as e:
            QMessageBox.critical(parent, "Error", f"Encryption failed: {str(e)}")
            print(f"Encryption failed: {str(e)}")
