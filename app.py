from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv  # Import the load_dotenv function
import os
from config import Config
from extensions import db, bcrypt
from routes import user_bp

# Load environment variables from the .env file
load_dotenv()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # Load the database URI from environment variable
    app.config.from_object(Config)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)

    # Register user routes blueprint
    app.register_blueprint(user_bp, url_prefix='/api/users')

    # Enable CORS for frontend
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

    return app

if __name__ == "__main__":
    app = create_app()
    migrate = Migrate(app, db)
    app.run(debug=True)