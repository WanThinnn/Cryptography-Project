import py_abac
from py_abac.storage.memory import MemoryStorage
from py_abac.policy import Policy

def create_policy_storage():
    policy_storage = MemoryStorage()

    policy_json = {
        "uid": "1",
        "description": "Allow access to data if user is authenticated",
        "effect": "allow",
        "rules": {
            "subject": {"$.authenticated": {"equals": True}},
            "action": {"$.method": {"equals": "GET"}},
            "resource": {"$.type": {"equals": "data"}},
            "context": {}
        },
        "conditions": {}
    }

    policy = Policy.from_json(policy_json)
    policy_storage.add(policy)

    return policy_storage
