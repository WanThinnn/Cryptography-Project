# initialize_policies.py
from ABAC.classABAC import AttributeBasedAccessControl
from policy_definitions import *

def initialize_policies():
    abac = AttributeBasedAccessControl()
    # abac.add_policy(master_policy_json)

    # abac.add_policy(admin_finance_policy_json)
    # abac.add_policy(admin_HR_policy_json)
    # abac.add_policy(admin_marketing_policy_json)

    # abac.add_policy(user_finance_policy_json)
    # abac.add_policy(user_HR_policy_json)
    # abac.add_policy(user_marketing_policy_json)

    # abac.add_policy(intern_finance_policy_json)
    # abac.add_policy(intern_HR_policy_json)
    # abac.add_policy(intern_marketing_policy_json)
    abac.add_policy(dataowner_policy_json)
    print("Add policies to mongo successfully")

if __name__ == "__main__":
    initialize_policies()
