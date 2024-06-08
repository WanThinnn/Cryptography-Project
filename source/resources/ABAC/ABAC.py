from py_abac import PDP, Request, Policy
from pymongo import MongoClient
from py_abac.storage.mongo import MongoStorage
from config import connect_string

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
