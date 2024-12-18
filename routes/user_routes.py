from flask import Blueprint, request, jsonify
from models.user import User  
from extensions import db, bcrypt

user_bp = Blueprint('user_bp', __name__)

# ** User Registration **
@user_bp.route('/register', methods=['POST'])
def register_user():
    user_name = request.json.get("username")
    password = request.json.get("password")
    email = request.json.get("email")

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email is already in use "})

    #Hash pass
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(user_name=user_name, password=hashed_password, email=email)

    try:
        db.session.add(new_user)
        db.session.comimt()
        return jsonify({"message": "User created", "id": new_user.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# User Sign In
@user_bp.route("/login", methods=["POST"])
def fetch_user():
    user_name = request.json.get("username")
    password = request.json.get("password")

    existing_user = User.query.filter_by(username=user_name).first()

    if not existing_user:
        return jsonify({"error": "That User Name does not exist"})

    # Checkin if pass matches hass pass
    if bcrypt.check_password_hash(existing_user.password, password):
        return True
        # return jsonify({"message": "Login Successful", "user": {"id": existing_user.id, "name": user.user_name}})


    else:
        return jsonify({"message": "invalid Password"})
    


# User log out
@user_bp.route("/logout", methods=["POST"])
def fetch_user():
    user_name = request.json.get("username")
    password = request.json.get("password")

    existing_user = User.query.filter_by(username=user_name).first()

    if not existing_user:
        return jsonify({"error": "That User Name does not exist"})

    # Checkin if pass matches hass pass
    if bcrypt.check_password_hash(existing_user.password, password):
        return True
        # return jsonify({"message": "Login Successful", "user": {"id": existing_user.id, "name": user.user_name}})


    else:
        return jsonify({"message": "invalid Password"})
    
    

# session.clear()