#main.py
import argparse
from policy import create_pdp, check_access, add_policy_to_db
from utils import get_wifi_ip
from db import get_sqlalchemy_engine
from sqlalchemy.exc import OperationalError

def main(args):
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
                    # "condition": "Equals",
                    # "value": "192.168.1.30"
                    "condition": "Exists"
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

    action_method = args.action_methods
    check_access(pdp, args.role, args.department, args.position, args.resource_type, action_method, ip_address)

    # if ip_address is not None:
    #     print(f"Wi-Fi IP address: {ip_address}")
    #     action_method = args.action_methods
    #     check_access(pdp, args.role, args.department, args.position, args.resource_type, action_method, ip_address)
    # else:
    #     print("Could not retrieve Wi-Fi IP address.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check access policy for a given request")
    parser.add_argument("role", type=str, help="Role of the subject")
    parser.add_argument("department", type=str, help="Department of the subject")
    parser.add_argument("position", type=str, help="Position of the subject")
    parser.add_argument("resource_type", type=str, help="Type of the resource")
    parser.add_argument("action_methods", type=str, nargs='?', help="Method of the action")

    args = parser.parse_args()

    main(args)
