from flask import Blueprint, request, jsonify
from models.user import User  
from extensions import db, bcrypt

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/register', methods=['POST', 'OPTIONS'])
def register_user():
    if request.method == 'OPTIONS':
        # Preflight request
        return preflight_response()

    data = request.get_json()
    if not data:
        return response_with_cors({"error": "Invalid JSON format"}, 400)

    user_name = data.get("username")
    password = data.get("password")
    email = data.get("email")

    if not user_name or not password or not email:
        return response_with_cors({"error": "All fields are required"}, 400)

    if User.query.filter_by(email=email).first() or User.query.filter_by(username=user_name).first():
        return response_with_cors({"error": "Username or email is already in use"}, 409)

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=user_name, password=hashed_password, email=email)

    try:
        db.session.add(new_user)
        db.session.commit()
        return response_with_cors({"message": "User created successfully", "id": new_user.id}, 201)
    except Exception as e:
        db.session.rollback()
        return response_with_cors({"error": f"Database error: {str(e)}"}, 500)

@user_bp.route('/login', methods=['POST', 'OPTIONS'])
def login_user():
    if request.method == 'OPTIONS':
        return preflight_response()

    data = request.get_json()
    if not data:
        return response_with_cors({"error": "Invalid JSON format"}, 400)

    user_name = data.get("username")
    password = data.get("password")

    if not user_name or not password:
        return response_with_cors({"error": "Username and password are required"}, 400)

    existing_user = User.query.filter_by(username=user_name).first()
    if not existing_user or not bcrypt.check_password_hash(existing_user.password, password):
        return response_with_cors({"error": "Invalid username or password"}, 401)

    return response_with_cors({"message": "Login successful"}, 200)

# Helper functions
def preflight_response():
    response = jsonify({"message": "Preflight OK"})
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    return response

def response_with_cors(payload, status=200):
    response = jsonify(payload)
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    return response, status
