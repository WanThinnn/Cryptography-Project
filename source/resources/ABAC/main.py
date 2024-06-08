# main.py
import sys
from ABAC import AttributeBasedAccessControl

def main():
    # Kiểm tra số lượng tham số CLI
    if len(sys.argv) != 4:
        print("Usage:\n \tpython3 main.py <username> <resource_type> <action_method>")
        sys.exit(1)

    # Lấy các tham số từ CLI
    username = sys.argv[1]
    resource_type = sys.argv[2]
    action_method = sys.argv[3]

    abac = AttributeBasedAccessControl()

    # Lấy thông tin nhân viên từ MySQL
    employee = abac.get_employee_attributes(username)
    if not employee:
        print(f"No employee found with username {username}")
        sys.exit(1)

    # Tạo yêu cầu truy cập
    request_access_format = {
        "subject": {
            "id": username,
            "attributes": {
                "role": employee['role'],
                "department": employee['department'],
                "position": employee['position'],
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

    if abac.is_request_allowed(request_access_format):
        print("Allowed")
    else:
        print("Denied")

if __name__ == "__main__":
    main()
