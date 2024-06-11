#fabac.py
from ABAC.classABAC import AttributeBasedAccessControl
import mysql.connector



class ProcessMongoDBCloud:
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

    def handle_abac(username, selected_resource):
        # Giả sử bạn có một instance của AttributeBasedAccessControl
        abac_instance = AttributeBasedAccessControl()
        employee_attributes = abac_instance.get_employee_attributes(username)
        print(f"Employee attributes: {employee_attributes}")
        # Logic xử lý ABAC tiếp theo
        return employee_attributes
    
    def get_columns(self, table_name):
        cursor = self.connection.cursor()
        cursor.execute(f"SHOW COLUMNS FROM `{table_name}`")
        columns = [column[0] for column in cursor.fetchall()]
        cursor.close()
        return columns
    
    def get_tables(self):
        cursor = self.connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        cursor.close()
        
        # Lọc ra các bảng có tên "login_table" và các bảng có tên bắt đầu bằng "key_"
        filtered_tables = [table for table in tables if "key" not in table.lower() and table != "login_table"]
            
        return filtered_tables
