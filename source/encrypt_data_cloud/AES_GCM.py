import json
import argparse
from py_abac import PDP, Policy, AccessRequest
from py_abac.storage.memory import MemoryStorage

def main(args):
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

    # Tạo đối tượng Policy từ JSON
    policy = Policy.from_json(enterprise_policy_json)

    # Tạo một bộ nhớ trong để lưu trữ các chính sách
    storage = MemoryStorage()

    # Thêm chính sách vào bộ nhớ
    storage.add(policy)

    # Tạo một Policy Decision Point (PDP) với bộ nhớ
    pdp = PDP(storage)

    # Định nghĩa yêu cầu truy cập theo định dạng đã cập nhật
    request_access_format = {
        "subject": {
            "id": "2",
            "attributes": {
                "role": args.role,
                "department": args.department,
                "position": args.position
            }
        },
        "resource": {
            "id": "2",
            "attributes": {
                "type": args.resource_type
            }
        },
        "action": {
            "id": "3",
            "attributes": {
                "method": args.action_method
            }
        },
        "context": {}
    }

    request = AccessRequest.from_json(request_access_format)

    # Kiểm tra chính sách và yêu cầu
    print("\nPolicy:")
    print(json.dumps(policy.to_json(), indent=4))

    print("\nAccess Request:")
    print(json.dumps(request_access_format, indent=4))

    # Đánh giá yêu cầu
    if pdp.is_allowed(request):
        print(f"\nAccess request is allowed")
    else:
        print(f"\nAccess request is denied")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check access policy for a given request")
    parser.add_argument("role", type=str, help="Role of the subject")
    parser.add_argument("department", type=str, help="Department of the subject")
    parser.add_argument("position", type=str, help="Position of the subject")
    parser.add_argument("resource_type", type=str, help="Type of the resource")
    parser.add_argument("action_method", type=str, help="Method of the action")

    args = parser.parse_args()
    main(args)
