import json
from py_abac import PDP, Policy, AccessRequest
from py_abac.storage.memory import MemoryStorage
from db import get_db_connection, close_db_connection, call_add_policy_procedure

def create_pdp():
    # Create an in-memory storage to store the policies
    storage = MemoryStorage()

    # Load policies from the database
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM policies")
        policies = cursor.fetchall()
        cursor.close()
        close_db_connection(connection)

        for policy_data in policies:
            policy = Policy.from_json({
                "uid": policy_data["id"],
                "description": policy_data["description"],
                "effect": policy_data["effect"],
                "rules": json.loads(policy_data["rules"]),
                "targets": json.loads(policy_data["target"])
            })
            storage.add(policy)
            print(f"Policy loaded into PDP: {policy_data}")

    # Create a Policy Decision Point (PDP) with the storage
    pdp = PDP(storage)

    return pdp

def add_policy_to_db(policy_json):
    policy = Policy.from_json(policy_json)
    call_add_policy_procedure(policy_json)

def check_access(pdp, role, department, position, resource_type, action_method):
    # Define the access request
    request_access_format = {
        "subject": {
            "id": "2",
            "attributes": {
                "role": role,
                "department": department,
                "position": position
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
