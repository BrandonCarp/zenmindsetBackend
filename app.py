from flask import Flask   
from config import Config 
from extensions import db
from routes.user_routes import user_bp  
from flask_cors import CORS

# Initialize the Flask app
app = Flask(__name__)

# Apply CORS to the app
CORS(app)

# Load configuration
app.config.from_object(Config)

# Initialize the database with the app context
db.init_app(app)

# Register the user routes blueprint with a URL prefix
app.register_blueprint(user_bp, url_prefix='/api/users')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates tables based on models if they don't already exist
    app.run(debug=True)
