#policy_definitions.py
master_policy_json = {
    "uid": "1",
    "description": "Director can view all documents of their department.",
    "effect": "allow",
    "rules": {
        "subject": {
            "$.role": {
                "condition": "Equals",
                "value": "master"
            },
            "$.department": {
                "condition": "Exists",
            },
            "$.position": {
                "condition": "Equals",
                "value": "director"
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
                "value": "view"
            }
        },
        "context": {}
    },
    "targets": {},
    "priority": 1
}


admin_finance_policy_json = {
    "uid": "2",
    "description": "Manager can view all documents of finance department.",
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
                "condition": "NotEquals",
                "value": "partners"
            },
            "$.department": {
                "condition": "Equals",
                "value": "finance"
            },
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


admin_HR_policy_json = {
    "uid": "3",
    "description": "Manager can view all documents of HR department.",
    "effect": "allow",
    "rules": {
        "subject": {
            "$.role": {
                "condition": "Equals",
                "value": "admin"
            },
            "$.department": {
                "condition": "Equals",
                "value": "HR"
            },
            "$.position": {
                "condition": "Equals",
                "value": "manager"
            },
        },
            
        "resource": {
            "$.type": {
                "condition": "NotEquals",
                "value": "partners"
            },
            "$.department": {
                "condition": "Equals",
                "value": "HR"
            },
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


admin_marketing_policy_json = {
    "uid": "4",
    "description": "Manager can view all documents of marketing department.",
    "effect": "allow",
    "rules": {
        "subject": {
            "$.role": {
                "condition": "Equals",
                "value": "admin"
            },
            "$.department": {
                "condition": "Equals",
                "value": "marketing"
            },
            "$.position": {
                "condition": "Equals",
                "value": "manager"
            },
        },
            
        "resource": {
            "$.type": {
                "condition": "NotEquals",
                "value": "partners"
            },
            "$.department": {
                "condition": "Equals",
                "value": "marketing"
            },
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


user_finance_policy_json = {
    "uid": "5",
    "description": "Staff can access basic documents and weekly meeting reports of finance department.",
    "effect": "allow",
    "rules": {
        "subject": {
            "$.role": {
                "condition": "Equals",
                "value": "user"
            },
            "$.department": {
                "condition": "Equals",
                "value": "finance"
            },
            "$.position": {
                "condition": "Equals",
                "value": "staff"
            },
        },
            
        "resource": {
                "$.type": {
                    "condition": "Equals",
                    "value": "products"
                },
                "$.department": {
                    "condition": "Equals",
                    "value": "finance"
                },
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


user_HR_policy_json = {
    "uid": "6",
    "description": "Staff can access basic documents and weekly meeting reports of HR department.",
    "effect": "allow",
    "rules": {
        "subject": {
            "$.role": {
                "condition": "Equals",
                "value": "user"
            },
            "$.department": {
                "condition": "Equals",
                "value": "HR"
            },
            "$.position": {
                "condition": "Equals",
                "value": "staff"
            },
        },
        "resource": {
                "$.type": {
                    "condition": "Equals",
                    "value": "products"
                },
                "$.department": {
                    "condition": "Equals",
                    "value": "HR"
                },
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


user_marketing_policy_json = {
    "uid": "7",
    "description": "Staff can access basic documents and weekly meeting reports of marketing department.",
    "effect": "allow",
    "rules": {
        "subject": {
            "$.role": {
                "condition": "Equals",
                "value": "user"
            },
            "$.department": {
                "condition": "Equals",
                "value": "marketing"
            },
            "$.position": {
                "condition": "Equals",
                "value": "staff"
            },
        },
            
        "resource": {
                "$.type": {
                    "condition": "Equals",
                    "value": "products"
                },
                "$.department": {
                    "condition": "Equals",
                    "value": "marketing"
                },
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


intern_finance_policy_json = {
    "uid": "8",
    "description": "Interns can access basic documents of their department.",
    "effect": "allow",
    "rules": {
        "subject": {
            "$.role": {
                "condition": "Equals",
                "value": "user"
            },
            "$.department": {
                "condition": "Equals",
                "value": "finance"
            },
            "$.position": {
                "condition": "Equals",
                "value": "intern"
            },
        },
            
        "resource": {
            "$.type": {
                "condition": "Equals",
                "value": "students"
            },
            "$.department": {
                "condition": "Equals",
                "value": "finance"
            },
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
    "priority": 4
}


intern_HR_policy_json = {
    "uid": "9",
    "description": "Interns can access basic documents of their department.",
    "effect": "allow",
    "rules": {
        "subject": {
            "$.role": {
                "condition": "Equals",
                "value": "user"
            },
            "$.department": {
                "condition": "Equals",
                "value": "HR"
            },
            "$.position": {
                "condition": "Equals",
                "value": "intern"
            },
        },
            
        "resource": {
            "$.type": {
                "condition": "Equals",
                "value": "students"
            },
            "$.department": {
                "condition": "Equals",
                "value": "HR"
            },
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
    "priority": 4
}


intern_marketing_policy_json = {
    "uid": "10",
    "description": "Interns can access basic documents of their department.",
    "effect": "allow",
    "rules": {
        "subject": {
            "$.role": {
                "condition": "Equals",
                "value": "user"
            },
            "$.department": {
                "condition": "Equals",
                "value": "marketing"
            },
            "$.position": {
                "condition": "Equals",
                "value": "intern"
            },
        },
            
        "resource": {
            "$.type": {
                "condition": "Equals",
                "value": "students"
            },
            "$.department": {
                "condition": "Equals",
                "value": "marketing"
            },
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
    "priority": 4
}




user_policy_json = {
    "uid": "12",
    "description": "User can access basic documents of their department.",
    "effect": "allow",
    "rules": {
        "subject": {
            "$.role": {
                "condition": "Equals",
                "value": "user"
            },
            "$.department": {
                "condition": "Equals",
                "value": "finance"
            },
            "$.position": {
                "condition": "Equals",
                "value": "staff"
            },
        },
            
        "resource": {
            "$.type": {
                "condition": "Equals",
                "value": "staffs"
            },
            "$.department": {
                "condition": "Equals",
                "value": "finance"
            },
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
    "priority": 4
}













