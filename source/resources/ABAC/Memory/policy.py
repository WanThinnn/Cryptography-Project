#policy.py
import json
from py_abac import PDP, Policy, AccessRequest
from py_abac.storage.memory import MemoryStorage

def create_pdp():
    # Define the policy for admin in the finance department
    enterprise_policy_json = {
        "uid": "4",
        "description": "Admin can perform actions on resources if they belong to the finance department and have the manager role.",
        "effect": "allow",
        "rules": {
            "subject": {
                "$.role": {
                    "condition": "Equals",
                    "value": "admin"
                },
                "$.department": {
                    "condition": "Equals",
                    "value": "finance"
                },
                "$.position": {
                    "condition": "Equals",
                    "value": "manager"
                },
                # "$.ip_address": {
                #     "condition": "Equals",
                #     "value": "192.168.1.30"
                # }
            },
            "resource": {
                "$.type": {
                    "condition": "Exists"
                }
            },
            "action": [
                {
                    "$.method": {
                        "condition": "Equals",
                        "value": "view"
                    }
                },
                {
                    "$.method": {
                        "condition": "Equals",
                        "value": "edit"
                    }
                }
            ],
            "context": {}
        },
        "targets": {},
        "priority": 0
    }

    # Create a Policy object from JSON
    policy = Policy.from_json(enterprise_policy_json)

    # Create an in-memory storage to store the policies
    storage = MemoryStorage()

    # Add the policy to the storage
    storage.add(policy)

    # Create a Policy Decision Point (PDP) with the storage
    pdp = PDP(storage)

    return pdp

def check_access(pdp, role, department, position, resource_type, action_method):
    # Define the access request
    request_access_format = {
        "subject": {
            "id": "2",
            "attributes": {
                "role": role,
                "department": department,
                "position": position,
                # "ip_address": ip_address
            }
        },
        "resource": {
            "id": "2",
            "attributes": {
                "type": resource_type
            }
        },
        "action": {
            "id": "3",
            "attributes": {
                "method": action_method
            }
        },
        "context": {}
    }

    request = AccessRequest.from_json(request_access_format)

    # Check the access request
    print(f"Checking access for action: {action_method}")
    if pdp.is_allowed(request):
        print(f"Access request for {action_method} is allowed\n")
    else:
        print(f"Access request for {action_method} is denied\n")
