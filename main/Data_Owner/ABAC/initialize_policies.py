# initialize_policies.py
from ABAC.classABAC import AttributeBasedAccessControl
from policy_definitions import *

def initialize_policies():
    abac = AttributeBasedAccessControl()
    abac.add_policy(doctor_policy_json)
    abac.add_policy(nurse_policy_json)

    print("Add policies to mongo successfully")

if __name__ == "__main__":
    initialize_policies()
