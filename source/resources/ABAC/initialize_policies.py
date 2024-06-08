# initialize_policies.py
from py_abac import Policy
from policy_storage import PolicyStorage
from policy_definitions import policy_json

def initialize_policies():
    policy_storage = PolicyStorage()
    storage = policy_storage.get_storage()
    
    policy = Policy.from_json(policy_json)
    
    storage.add(policy)

if __name__ == "__main__":
    initialize_policies()
