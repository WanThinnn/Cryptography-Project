# main.py
import sys
from access_control import AccessControl



def main():
    # Kiểm tra số lượng tham số CLI
    if len(sys.argv) != 6:
        print("Usage:\n \tpython3 main.py <role> <department> <position> <resource_type> <action_method>")
        sys.exit(1)

    # Lấy các tham số từ CLI
    role = sys.argv[1]
    department = sys.argv[2]
    position = sys.argv[3]
    resource_type = sys.argv[4]
    action_method = sys.argv[5]


    # Sample access request JSON for a patient
    request_access_format = {
        "subject": {
                "id": "2",
                "attributes": {
                    "role": role,
                    "department": department,
                    "position": position,
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

    ac = AccessControl()
    if ac.is_request_allowed(request_access_format):
        print("Allowed")
    else:
        print("Denied")

if __name__ == "__main__":
    main()
