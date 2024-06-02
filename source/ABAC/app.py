from flask import Flask, request, jsonify
from py_abac.context import EvaluationContext
from py_abac.request import AccessRequest
from policies import create_policy_storage
from auth import authenticate
import datetime

app = Flask(__name__)

policy_storage = create_policy_storage()
enforcer = py_abac.Enforcer(policy_storage) # type: ignore

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user = authenticate(email, password)
    
    if user:
        user['authenticated'] = True
        return jsonify(user), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/data', methods=['GET'])
def get_data():
    user = request.json.get('user')
    if not user:
        return jsonify({"error": "User not authenticated"}), 403

    request_json = {
        "subject": user,
        "action": {"method": "GET"},
        "resource": {"type": "data"},
        "context": {}
    }

    request = AccessRequest.from_json(request_json)
    context = EvaluationContext(request, datetime.datetime.utcnow())

    if enforcer.is_allowed(context):
        # Thay thế bằng logic lấy dữ liệu từ cơ sở dữ liệu
        data = {"message": "Access granted, here is your data!"}
        return jsonify(data), 200
    else:
        return jsonify({"error": "Access denied"}), 403

if __name__ == '__main__':
    app.run(debug=True)
