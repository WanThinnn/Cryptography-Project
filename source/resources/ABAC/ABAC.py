# ABAC.py
from py_abac import PDP, Request, Policy
from pymongo import MongoClient
from py_abac.storage.mongo import MongoStorage
import mysql.connector
from config import connect_string, mysql_config

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
