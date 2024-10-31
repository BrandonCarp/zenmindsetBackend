# routes/user_routes.py
from flask import Blueprint, request, jsonify
from models.user import User  # Import the User model
from app import db  # Import db from app

user_bp = Blueprint('user_bp', __name__)

# Route for managing users
@user_bp.route("/register", methods=["POST"])
def register_user():
    # Get data from the request
    user_name = request.json.get("user_name")
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

# Route for managing items (keep your existing item routes here)
@item_bp.route("/", methods=["POST", "GET"])
def manage_items():
    if request.method == "POST":
        description = request.json.get("description")
        new_item = Item(description=description)
        try:
            db.session.add(new_item)
            db.session.commit()
            return jsonify({"message": "Item created", "id": new_item.id}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    items = Item.query.order_by(Item.created_at).all()
    items_list = [{"id": item.id, "description": item.description, "completed": item.completed} for item in items]
    return jsonify(items_list)
