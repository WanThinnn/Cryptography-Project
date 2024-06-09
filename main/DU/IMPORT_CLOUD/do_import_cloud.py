import mysql.connector
import pandas as pd
from PyQt6.QtWidgets import QFileDialog, QMessageBox

class ProcessCloud:
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
    def deconnect_from_db(self):
        self.connection.close()
        self.connection = self.connect_to_db()

    def get_tables(self):
        cursor = self.connection.cursor()
        cursor.execute(f"SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        cursor.close()
        return tables



    def get_columns(self, table_name):
        cursor = self.connection.cursor()
        cursor.execute(f"SHOW COLUMNS FROM `{table_name}`")
        columns = [column[0] for column in cursor.fetchall()]
        cursor.close()
        return columns

    def get_table_data(self, table_name):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM `{table_name}`")
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()
        return data, columns

    def select_plaintextfile(self, parent):
        file, _ = QFileDialog.getOpenFileName(parent, "Select Plaintext File", "", "CSV Files (*.csv);;All Files (*)")
        parent.ui.lineEdit_plaintextfile.setText(file)

        if file:
            self.plaintext_file = file
            print(f"Plaintext file selected: {file}")

    def import_data(self, ui):
        if not self.plaintext_file:
            self.select_plaintextfile(ui)
        
        if self.plaintext_file:
            table_name = ui.comboBox_table.currentText()
            self.upload_csv_to_db(self.plaintext_file, table_name)
            self.show_message("Success", "Data has been encrypted and uploaded successfully.")
        
    def upload_csv_to_db(self, file_path, table_name):
        # Đọc dữ liệu từ file CSV
        df = pd.read_csv(file_path)

        # Tạo bảng trong MySQL
        cursor = self.connection.cursor()
        columns = ", ".join([f"`{col}` VARCHAR(255)" for col in df.columns])
        create_table_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({columns})"
        cursor.execute(create_table_query)
        
        # Chèn dữ liệu vào bảng
        for _, row in df.iterrows():
            values = "', '".join(str(v) for v in row.tolist())
            insert_query = f"INSERT INTO `{table_name}` VALUES ('{values}')"
            cursor.execute(insert_query)
        
        self.connection.commit()
        cursor.close()
        print(f"Data from {file_path} uploaded successfully to {table_name}.")

    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()

    def close_connection(self):
        self.connection.close()

    def query_db_to_csv(self, query, file_path):
        cursor = self.connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()
        
        # Tạo DataFrame từ dữ liệu
        df = pd.DataFrame(rows, columns=columns)
        
        # Lưu DataFrame vào tệp CSV
        df.to_csv(file_path, index=False)
        print(f"Query results saved to {file_path}.")
        return file_path

    def select_decryptedfile(self, ui):
        file, _ = QFileDialog.getSaveFileName(ui, "Select Decrypted File", "", "CSV Files (*.csv);;All Files (*)")
        if file:
            self.decrypted_file = file
            print(f"Decrypted file selected: {file}")

    def select_keyfile(self, ui):
        file, _ = QFileDialog.getOpenFileName(ui, "Select Key File", "", "Key Files (*.key);;All Files (*)")
        if file:
            self.keyfile = file
            print(f"Key file selected: {file}")

    def decrypt_data_du(self, ui):
        selected_columns = self.get_selected_columns()

        # Lấy tên bảng từ comboBox
        table_name = ui.comboBox_table.currentText()

        if not self.encrypted_file:
            # Truy vấn cơ sở dữ liệu và lưu dữ liệu vào file CSV
            query = f"SELECT * FROM `{table_name}`"  # Sử dụng tên bảng từ comboBox
            self.encrypted_file = self.query_db_to_csv(query, "temporary_encrypted_file.csv")

        if not self.decrypted_file:
            self.select_decryptedfile(ui)
        if not self.keyfile:
            self.select_keyfile(ui)

        if self.encrypted_file and self.keyfile:
            self.aes_gcm.decrypt_data(self.decrypted_file, selected_columns, None, self.encrypted_file, self.keyfile)
            self.show_message("Success", "Data has been decrypted successfully.")
