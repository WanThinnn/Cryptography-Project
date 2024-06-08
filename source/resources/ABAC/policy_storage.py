# policy_storage.py
from pymongo import MongoClient
from py_abac.storage.mongo import MongoStorage
from config import connect_string

class PolicyStorage:
    def __init__(self):
        self.client = MongoClient(connect_string)
        self.storage = MongoStorage(self.client, db_name="policy_repository", collection="abac")
    
    def add_policy(self, policy):
        self.storage.add(policy)
    
    def get_storage(self):
        return self.storage
