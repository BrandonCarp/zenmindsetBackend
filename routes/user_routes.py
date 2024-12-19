from flask import Blueprint, request, jsonify, session
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
        db.session.commit()
        return jsonify({"message": "User created", "id": new_user.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# User Sign In
@user_bp.route("/login", methods=["POST"])
def fetch_user():
    user_name = request.json.get("username")
    password = request.json.get("password")

    existing_user = User.query.filter_by(username=user_name).first()

    if not existing_user or not bcrypt.check_password_hash(existing_user.password, password):
        return jsonify({"error": "Invalid username or password"}), 401


    session['user_id'] = existing_user.id

    return jsonify({"message": "Login successful", "user_id": existing_user.id})

    


# User log out
@user_bp.route("/logout", methods=["POST"])
def logout_user():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out successfully"}), 200
    


# Pseudocode for handling front end user data ie: posts ect 
# @user_bp.route("/profile", methods=["GET"])
# def get_profile():
#     user_id = session.get('user_id')
#     if not user_id:
#         return jsonify({"error": "Unauthorized"}), 401
    
#     user = User.query.get(user_id)
#     if not user:
#         return jsonify({"error": "User not found"}), 404

#     # Fetch additional data like posts
#     posts = [{"title": "Post 1"}, {"title": "Post 2"}]  # Replace with actual query logic
#     return jsonify({
#         "username": user.user_name,
#         "email": user.email,
#         "posts": posts
#     })


# Fetching blogs

# @user_bp.route('/profile/blogs', methods=['GET'])
# def get_user_blogs():
#     # Ensure the user is logged in by checking the session
#     if 'user_id' not in session:
#         return jsonify({"error": "Unauthorized"}), 401
    
#     user_id = session['user_id']
    
#     # Query the blogs related to the current user
#     blogs = Blog.query.filter_by(user_id=user_id).all()  # Assuming a Blog model with a `user_id` field
    
#     # Convert blogs to a dictionary or any required format to send back as JSON
#     blog_list = [{"id": blog.id, "title": blog.title, "content": blog.content} for blog in blogs]

#     return jsonify({"blogs": blog_list})