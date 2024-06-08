from ABAC import AttributeBasedAccessControl
from policy_definitions import policy_json

def initialize_policies():
    abac = AttributeBasedAccessControl()
    abac.add_policy(policy_json)

if __name__ == "__main__":
    initialize_policies()
