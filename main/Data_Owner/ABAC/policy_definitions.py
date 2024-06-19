#policy_definitions.py
master_doctor_policy_json = {
    "uid": "1",
    "description": "Head of Cardiology department can view all documents of their department.",
    "effect": "allow",
    "rules": {
        "subject": {
            "$.role": {
                "condition": "Equals",
                "value": "head-of-cardiology"
            },
            "$.department": {
                "condition": "Exists",
            },
            "$.position": {
                "condition": "Equals",
                "value": "doctor"
            },
        },
            
        "resource": {
            "$.type": {
                "condition": "Exists",
            }
        },
        "action": {
            "$.method": {
                "condition": "Equals",
                "value": "upload"
            }
        },
        "context": {}
    },
    "targets": {},
    "priority": 1
}






nurse_policy_json = {
    "uid": "2",
    "description": "nurse can access basic documents and weekly meeting reports of their department.",
    "effect": "allow",
    "rules": {
        "subject": {
            "$.role": {
                "condition": "Equals",
                "value": "nurse"
            },
            "$.department": {
                "condition": "Equals",
                "value": "cardiology"
            },
            "$.position": {
                "condition": "Equals",
                "value": "nurse"
            },
        },
            
        "resource": {
                "$.type": {
                    "condition": "Equals",
                    "value":  "cardiovascular_patients"
                },
                "$.department": {
                    "condition": "Equals",
                    "value": "cardiology"
                }
        },
        "action": {
            "$.method": {
                "condition": "Equals",
                "value": "view"
            }
        },
        "context": {}
    },
    "targets": {},
    "priority": 2
}



nurse_policy_json_2 = {
    "uid": "3",
    "description": "nurse can access basic documents and weekly meeting reports of their department.",
    "effect": "allow",
    "rules": {
        "subject": {
            "$.role": {
                "condition": "Equals",
                "value": "nurse"
            },
            "$.department": {
                "condition": "Equals",
                "value": "cardiology"
            },
            "$.position": {
                "condition": "Equals",
                "value": "nurse"
            },
        },
            
        "resource": {
                "$.type": {
                    "condition": "Equals",
                    "value":  "keys_cardiovascular_patients"
                },
                "$.department": {
                    "condition": "Equals",
                    "value": "cardiology"
                }
        },
        "action": {
            "$.method": {
                "condition": "Equals",
                "value": "view"
            }
        },
        "context": {}
    },
    "targets": {},
    "priority": 3
}