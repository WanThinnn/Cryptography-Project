import argparse
from policy import create_pdp, check_access, add_policy_to_db

def main(args):
    # Create the PDP
    pdp = create_pdp()

    # Define the policy to add to the database
    policy_json = {
        "uid": "4",
        "description": "Admin can perform actions on resources if they belong to the finance department and have the manager role.",
        "effect": "allow",
        "rules": {
            "subject": {
                "$.role": {"condition": "Equals", "value": "admin"},
                "$.department": {"condition": "Equals", "value": "finance"},
                "$.position": {"condition": "Equals", "value": "manager"}
            },
            "resource": {
                "$.type": {"condition": "Exists"}
            },
            "action": [
                {"$.method": {"condition": "Equals", "value": "view"}},
                {"$.method": {"condition": "Equals", "value": "edit"}}
            ],
            "context": {}
        },
        "targets": {},
        "priority": 0
    }

    # Add the policy to the database
    add_policy_to_db(policy_json)

    # Check access for the given action
    action_method = args.action_methods
    check_access(pdp, args.role, args.department, args.position, args.resource_type, action_method)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check access policy for a given request")
    parser.add_argument("role", type=str, help="Role of the subject")
    parser.add_argument("department", type=str, help="Department of the subject")
    parser.add_argument("position", type=str, help="Position of the subject")
    parser.add_argument("resource_type", type=str, help="Type of the resource")
    parser.add_argument("action_methods", type=str, nargs='?', help="Method of the action")

    args = parser.parse_args()

    main(args)
