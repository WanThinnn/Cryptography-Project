# access_control.py
from py_abac import PDP, Request
from policy_storage import PolicyStorage

class AccessControl:
    def __init__(self):
        self.policy_storage = PolicyStorage()
        self.pdp = PDP(self.policy_storage.get_storage())
    
    def is_request_allowed(self, request_json):
        request = Request.from_json(request_json)
        return self.pdp.is_allowed(request)
