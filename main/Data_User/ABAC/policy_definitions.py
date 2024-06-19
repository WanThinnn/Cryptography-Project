doctor_policy_json = {
    "uid": "1",
    "description": "Doctor can view and upload all documents of their hospital.",
    "effect": "allow",
    "rules": {
        "subject": {
            "$.role": {
                "condition": "Equals",
                "value": "doctor"
            },
            "$.department": {
                "condition": "Equals",
                "value": "cardiology"
            },
            "$.position": {
                "condition": "Equals",
                "value": "doctor"
            },
        },
            
        "resource": {
            "$.type": {
                "condition": "NotEquals",
                "value": "cardiovascular_patients"
            },
            "$.department": {
                "condition": "Equals",
                "value": "cardiology"
            },
        },
        "action": {
            "$.method": [
            {
                "condition": "Equals",
                "value": "view"
            },
            {
                "condition": "Equals",
                "value": "upload"
            }
            ]
        },
        "context": {}
    },
    "targets": {},
    "priority": 1
}

nurse_policy_json = {
    "uid": "2",
    "description": "Nurse can view all documents of their hospital.",
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
                "condition": "NotEquals",
                "value": "cardiovascular_patients"
            },
            "$.department": {
                "condition": "Equals",
                "value": "cardiology"
            },
        },
        "action": {
            "$.method": 
            {
                "condition": "Equals",
                "value": "view"
            }
        },
        "context": {}
    },
    "targets": {},
    "priority": 2
}

