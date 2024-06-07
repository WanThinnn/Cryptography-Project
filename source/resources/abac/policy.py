import json
from py_abac import PDP, Policy, AccessRequest
from py_abac.storage.sql import SQLStorage
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

def check_db_connection(engine):
    try:
        connection = engine.connect()
        connection.close()
        return True
    except OperationalError:
        return False

def create_pdp(engine):
    if not check_db_connection(engine):
        print("Database connection is not available.")
        return None

    Session = sessionmaker(bind=engine)
    session = Session()
    storage = SQLStorage(session)

    # Tải tất cả các chính sách từ bảng policies
    try:
        result = session.execute("SELECT * FROM policies")
        policies = result.fetchall()
        for policy in policies:
            policy_data = {
                "uid": policy[0],
                "description": policy[1],
                "effect": policy[2],
                "rules": json.loads(policy[3]),
                "targets": json.loads(policy[4])
            }
            policy_obj = Policy.from_json(policy_data)
            storage.add(policy_obj)
            print(f"Policy loaded into PDP: {policy_data}")
    except Exception as e:
        print(f"Error fetching policies from database: {e}")
    finally:
        session.close()

    return PDP(storage)



def add_policy_to_db(engine, policy_json):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        policy = Policy.from_json(policy_json)
        session.execute(
            "CALL AddPolicy(:id, :description, :effect, :rules, :target)",
            {
                'id': policy.uid,
                'description': policy.description,
                'effect': policy.effect,
                'rules': json.dumps(policy_json['rules']),
                'target': json.dumps(policy_json['targets']) if 'targets' in policy_json else json.dumps({})
            }
        )
        session.commit()
        print("Policy added to database successfully.")
        
        # Kiểm tra lại chính sách đã lưu
        result = session.execute("SELECT * FROM policies WHERE id = :id", {'id': policy.uid}).fetchone()
        print(f"Policy in DB: {result}")
    finally:
        session.close()

def check_access(pdp, role, department, position, resource_type, action_method, ip_address):
    # Định nghĩa yêu cầu truy cập
    request_access_format = {
        "subject": {
            "id": "2",
            "attributes": {
                "role": role,
                "department": department,
                "position": position,
                "ip_address": ip_address
            }
        },
        "resource": {
            "id": "2",
            "attributes": {
                "type": resource_type
            }
        },
        "action": {
            "id": "3",
            "attributes": {
                "method": action_method
            }
        },
        "context": {}
    }

    request = AccessRequest.from_json(request_access_format)
    print(f"Access request: {request_access_format}")

    # Kiểm tra yêu cầu
    if pdp:
        print(f"Checking access for action: {action_method}")
        is_allowed = pdp.is_allowed(request)
        print(f"PDP Decision: {is_allowed}")
        if is_allowed:
            print(f"Access request for {action_method} is allowed\n")
        else:
            print(f"Access request for {action_method} is denied\n")
    else:
        print("PDP is not available. Cannot check access.")
