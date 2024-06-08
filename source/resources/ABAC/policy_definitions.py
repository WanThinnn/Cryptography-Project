#policy_definitions.py
policy_json = {
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
        },
        "resource": {
            "$.type": {
                "condition": "Exists",
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
