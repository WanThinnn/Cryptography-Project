from src.abac.user import User
from src.abac.resource import Resource
from src.abac.policies import ABACPolicy
from src.abac.rules import rule_admin_access, rule_finance_access, rule_office_hours_access
from src.database.db import connect_to_db

def fetch_users_from_db():
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT username, role FROM users")
    users = []
    for row in cursor.fetchall():
        attributes = {"role": row["role"]}
        users.append(User(row["username"], attributes))
    cursor.close()
    conn.close()
    return users

def fetch_resources_from_db():
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT resource_name, sensitivity FROM resources")
    resources = []
    for row in cursor.fetchall():
        attributes = {"sensitivity": row["sensitivity"]}
        resources.append(Resource(row["resource_name"], attributes))
    cursor.close()
    conn.close()
    return resources

def check_access(user, resource):
    policy = ABACPolicy("Default Policy", [rule_admin_access, rule_finance_access, rule_office_hours_access])
    if policy.is_access_allowed(user, resource):
        print(f"Access granted to {user.username} for {resource.resource_name}")
    else:
        print(f"Access denied to {user.username} for {resource.resource_name}")

def main():
    users = fetch_users_from_db()
    resources = fetch_resources_from_db()
    
    for user in users:
        for resource in resources:
            check_access(user, resource)

if __name__ == "__main__":
    main()
