from flask import Blueprint, request, jsonify
from models.user import User  
from extensions import db

user_bp = Blueprint('user_bp', __name__)

# Route for managing users
@user_bp.route("/register", methods=["POST"])
def register_user():
    # Get data from the request
    user_name = request.json.get("username")
    password = request.json.get("password")
    email = request.json.get("email")

    # Create a new user instance
    new_user = User(user_name=user_name, password=password, email=email)

    try:
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created", "id": new_user.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
