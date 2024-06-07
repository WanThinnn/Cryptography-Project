import py_abac
from py_abac import PDP, Request
from py_abac.policy import Policy
from py_abac.storage.sql import SQLStorage
import mysql.connector
import json

# Kết nối tới MySQL
conn = mysql.connector.connect(
    host="company-database.clce6ae44hhz.ap-southeast-2.rds.amazonaws.com",
    user="admin",
    password="24122003",
    database="company_db"
)

# Khởi tạo PDP với bộ lưu trữ SQL sử dụng MySQL
storage = SQLStorage(conn)
pdp = PDP(storage)

# Tải chính sách từ tệp JSON và thêm vào bộ lưu trữ
with open('policies.json') as f:
    policies = json.load(f)
    for policy_json in policies:
        policy = Policy.from_json(policy_json)
        storage.add(policy)

# Hàm kiểm tra quyền truy cập
def check_access(user_role):
    request_json = {
        "subject": {
            "id": "user-1",
            "attributes": {
                "role": user_role
            }
        },
        "resource": {
            "id": "resource-1",
            "attributes": {}
        },
        "action": {
            "id": "action-1",
            "attributes": {}
        },
        "context": {}
    }

    request = Request.from_json(request_json)
    decision = pdp.is_allowed(request)
    return decision

# Kiểm tra quyền truy cập với các vai trò khác nhau
roles_to_check = ["employee", "guest", "admin"]

for role in roles_to_check:
    print(f"Access check for role '{role}': {check_access(role)}")

# Đóng kết nối MySQL
conn.close()
