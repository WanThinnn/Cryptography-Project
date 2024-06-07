import sys
from policy import create_pdp, check_access, add_policy_to_db
from utils import get_wifi_ip
from db import get_sqlalchemy_engine
from sqlalchemy.exc import OperationalError

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

    # Cấu hình kết nối cơ sở dữ liệu
    db_config = {
        'host': "company-database.clce6ae44hhz.ap-southeast-2.rds.amazonaws.com",
        'user': "admin",
        'password': "24122003",
        'database': "company_db"
    }

    try:
        engine = get_sqlalchemy_engine(db_config)
        connection = engine.connect()
        print("Connected to database successfully.")
        connection.close()
    except OperationalError as e:
        print(f"Failed to connect to database: {e}")
        return

    # Tạo PDP từ cơ sở dữ liệu
    pdp = create_pdp(engine)

    # Tạo và thêm chính sách vào cơ sở dữ liệu
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
                "$.ip_address": {
                    "condition": "Equals",
                    "value": "192.168.1.30"
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

    add_policy_to_db(engine, policy_json)

    ip_address = get_wifi_ip()

    if ip_address is not None:
        print(f"Wi-Fi IP address: {ip_address}")
        check_access(pdp, role, department, position, resource_type, action_method, ip_address)
    else:
        print("Could not retrieve Wi-Fi IP address.")

if __name__ == "__main__":
    main()
