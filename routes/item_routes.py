# routes/item_routes.py
from flask import Blueprint, request, jsonify
from models.item import Item
from app import db  # Import db from app

item_bp = Blueprint('item_bp', __name__)

# Route for managing items
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


@app.route("/")
def home():
    return "Welcome Home"