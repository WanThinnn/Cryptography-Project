import json
from py_abac import PDP, Policy, AccessRequest
from py_abac.storage.memory import MemoryStorage

# Định nghĩa chính sách cho admin trong doanh nghiệp
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
            }
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

policy = Policy.from_json(enterprise_policy_json)

# Tạo một bộ nhớ trong để lưu trữ các chính sách
storage = MemoryStorage()

# Thêm chính sách vào bộ nhớ
storage.add(policy)

# Tạo một Policy Decision Point (PDP) với bộ nhớ
pdp = PDP(storage)

# Nhập các thuộc tính từ bàn phím
subject_role = input("Enter subject role (e.g., admin): ")
subject_department = input("Enter subject department (e.g., finance): ")
subject_position = input("Enter subject position (e.g., manager): ")
resource_type = input("Enter resource type (e.g., financial_report): ")
action_method = input("Enter action method (e.g., view, edit): ")

# Định nghĩa yêu cầu truy cập theo định dạng đã cập nhật
request_access_format = {
    "subject": {
        "id": "2",
        "attributes": {
            "role": subject_role,
            "department": subject_department,
            "position": subject_position
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

# Kiểm tra chính sách và yêu cầu
print("Policy:")
print(json.dumps(policy.to_json(), indent=4))

print("Access Request:")
print(json.dumps(request_access_format, indent=4))

# Đánh giá yêu cầu
if pdp.is_allowed(request):
    print(f"Access request is allowed")
else:
    print(f"Access request is denied")
