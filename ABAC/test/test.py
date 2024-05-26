from datetime import datetime

class User:
    def __init__(self, username, attributes):
        self.username = username
        self.attributes = attributes

class Resource:
    def __init__(self, resource_name, attributes):
        self.resource_name = resource_name
        self.attributes = attributes

class ABACPolicy:
    def __init__(self, policy_name, rules):
        self.policy_name = policy_name
        self.rules = rules
    
    def is_access_allowed(self, user, resource):
        for rule in self.rules:
            if rule(user, resource):
                return True
        return False

# Define rules
def rule_admin_access(user, resource):
    return user.attributes.get("role") == "admin"

def rule_finance_access(user, resource):
    return (user.attributes.get("department") == "finance" and 
            resource.attributes.get("sensitivity") == "low")

def rule_office_hours_access(user, resource):
    current_hour = datetime.now().hour
    return 9 <= current_hour < 17

# Create users
user1 = User("Alice", {"role": "admin"})
user2 = User("Bob", {"department": "finance"})
user3 = User("Charlie", {"department": "engineering"})

# Create resources
resource1 = Resource("Financial Report", {"sensitivity": "high"})
resource2 = Resource("General Report", {"sensitivity": "low"})

# Define policies
policy = ABACPolicy("Default Policy", [rule_admin_access, rule_finance_access, rule_office_hours_access])

# Check access
def check_access(user, resource):
    if policy.is_access_allowed(user, resource):
        print(f"Access granted to {user.username} for {resource.resource_name}")
    else:
        print(f"Access denied to {user.username} for {resource.resource_name}")

# Test access control
check_access(user1, resource1)  # Admin should have access
check_access(user2, resource1)  # Finance should not have access to high sensitivity resource
check_access(user2, resource2)  # Finance should have access to low sensitivity resource
check_access(user3, resource2)  # Engineer should not have access outside office hours
