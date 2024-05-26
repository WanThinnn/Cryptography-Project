from abac.user import User
from abac.resource import Resource
from abac.policies import ABACPolicy
from database.db import fetch_users, fetch_resources

# Lấy dữ liệu từ cơ sở dữ liệu
users_data = fetch_users()
resources_data = fetch_resources()

# Tạo danh sách người dùng và tài nguyên từ dữ liệu cơ sở dữ liệu
users = [User(username=user['username'], role=user['role'], department=user['department']) for user in users_data]
resources = [Resource(resource_name=resource['resource_name'], sensitivity=resource['sensitivity']) for resource in resources_data]

# Định nghĩa chính sách
policy = {'role': 'user', 'department': 'finance'}

# Tạo đối tượng ABAC và thêm chính sách
abac_policy = ABACPolicy()
abac_policy.add_policy(policy)

# Đánh giá quyền truy cập cho mỗi người dùng và tài nguyên
for user in users:
    for resource in resources:
        if abac_policy.evaluate(user, resource):
            print(f"Access granted for {user.username} to {resource.resource_name}")
        else:
            print(f"Access denied for {user.username} to {resource.resource_name}")
