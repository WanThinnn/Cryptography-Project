# classABAC.py
from py_abac import PDP, Request, Policy
from pymongo import MongoClient
from py_abac.storage.mongo import MongoStorage
import mysql.connector
import os, sys
from config import connect_string, mysql_config


# Lấy đường dẫn hiện tại của tệp đang chạy
current_dir = os.path.dirname(os.path.abspath(__file__))
# Lấy đường dẫn của thư mục cha
parent_dir = os.path.dirname(current_dir)
# Thêm đường dẫn của thư mục cha vào sys.path
sys.path.append(parent_dir)
home = os.path.join(parent_dir, 'HOME')
sys.path.append(home)
from HOME.login import *
from HOME.signup import *

class AttributeBasedAccessControl:
    def __init__(self):
        self.client = MongoClient(connect_string)
        self.storage = MongoStorage(self.client, db_name="policy_repository", collection="abac")
        self.pdp = PDP(self.storage)
    
    def add_policy(self, policy_json):
        policy = Policy.from_json(policy_json)
        self.storage.add(policy)
    
    def is_request_allowed(self, request_json):
        request = Request.from_json(request_json)
        return self.pdp.is_allowed(request)
    
    def get_employee_attributes(self, username):
        cnx = mysql.connector.connect(**mysql_config)
        cursor = cnx.cursor(dictionary=True)

        query = "SELECT role, department, position FROM employee WHERE username = %s"
        cursor.execute(query, (username,))

        employee = cursor.fetchone()
        cursor.close()
        cnx.close()

        return employee
