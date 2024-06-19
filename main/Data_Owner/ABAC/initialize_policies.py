# initialize_policies.py
from classABAC import AttributeBasedAccessControl
from policy_definitions import *

def initialize_policies():
    abac = AttributeBasedAccessControl()
    abac.add_policy(nurse_policy_json)
    abac.add_policy(nurse_policy_json_2)
    # abac.add_policy(master_doctor_policy_json)

    print("Add policies to mongo successfully")

if __name__ == "__main__":
    initialize_policies()
