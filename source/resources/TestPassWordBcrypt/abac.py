import mysql.connector
from py_abac import PDP, Policy, AccessRequest
from py_abac.storage.sql import SQLStorage
from sqlalchemy import create_engine
import json

# Kết nối tới cơ sở dữ liệu MySQL
mydb = mysql.connector.connect(
    host="company-database.clce6ae44hhz.ap-southeast-2.rds.amazonaws.com",
    user="admin",
    password="24122003",
    database="company_db"
)

cursor = mydb.cursor(dictionary=True)

# Lấy thông tin người dùng từ bảng users
cursor.execute("SELECT id, username, role FROM users")
users = cursor.fetchall()

# Tạo engine kết nối tới cơ sở dữ liệu MySQL với SQLAlchemy
engine = create_engine('mysql+mysqlconnector://admin:24122003@company-database.clce6ae44hhz.ap-southeast-2.rds.amazonaws.com/company_db')

# Tạo SQLStorage với SQLAlchemy engine
storage = SQLStorage(engine)

# Khởi tạo bảng lưu trữ policies (chỉ cần làm một lần)
storage.create_tables()

# Định nghĩa các chính sách
policy_json_admin = '''
{
    "id": "1",
    "description": "Allow read and write access to data for admins",
    "effect": "allow",
    "rules": {
        "subject": {
            "attributes": {
                "role": {
                    "equals": "admin"
                }
            }
        },
        "action": {
            "in": ["read", "write"]
        },
        "resource": {
            "attributes": {
                "type": {
                    "equals": "data"
                }
            }
        }
    },
    "conditions": {},
    "meta": {
        "created_at": "2024-06-05T12:00:00",
        "created_by": "admin"
    }
}
'''

policy_json_employee = '''
{
    "id": "2",
    "description": "Allow read access to data for employees",
    "effect": "allow",
    "rules": {
        "subject": {
            "attributes": {
                "role": {
                    "equals": "employee"
                }
            }
        },
        "action": {
            "equals": "read"
        },
        "resource": {
            "attributes": {
                "type": {
                    "equals": "data"
                }
            }
        }
    },
    "conditions": {},
    "meta": {
        "created_at": "2024-06-05T12:00:00",
        "created_by": "admin"
    }
}
'''

policy_json_manager = '''
{
    "id": "3",
    "description": "Allow read and write access to data for managers",
    "effect": "allow",
    "rules": {
        "subject": {
            "attributes": {
                "role": {
                    "equals": "manager"
                }
            }
        },
        "action": {
            "in": ["read", "write"]
        },
        "resource": {
            "attributes": {
                "type": {
                    "equals": "data"
                }
            }
        }
    },
    "conditions": {},
    "meta": {
        "created_at": "2024-06-05T12:00:00",
        "created_by": "admin"
    }
}
'''

# Thêm các policy vào SQLStorage
storage.add(Policy.from_json(policy_json_admin))
storage.add(Policy.from_json(policy_json_employee))
storage.add(Policy.from_json(policy_json_manager))

# Tạo PDP
pdp = PDP(storage)

def check_access(user, action, resource_type):
    request_json = json.dumps({
        "subject": {
            "id": user['id'],
            "attributes": {
                "role": user['role']
            }
        },
        "action": action,
        "resource": {
            "id": "resource1",
            "attributes": {
                "type": resource_type
            }
        },
        "context": {}
    })

    request = AccessRequest.from_json(request_json)
    decision = pdp.is_allowed(request)
    return decision

# Kiểm tra truy cập cho từng người dùng
for user in users:
    action = "read"  # Hoặc "write"
    resource_type = "data"
    access_granted = check_access(user, action, resource_type)
    print(f"User {user['username']} with role {user['role']} {'is allowed' if access_granted else 'is not allowed'} to {action} {resource_type}.")
