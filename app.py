from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from extensions import db, bcrypt
from routes import user_bp

def create_app():
    app = Flask(__name__, instance_relative_config=True)  # Enable instance-relative config
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    app.config.from_object(Config)  # Default config (e.g., development)
    app.config.from_pyfile('config.py', silent=True)  # Load sensitive config from instance/config.py
    db.init_app(app)
    bcrypt.init_app(app)
    app.register_blueprint(user_bp, url_prefix='/api/users')
    return app

if __name__ == "__main__":
    app = create_app()
    migrate = Migrate(app, db)  # Initialize migrations
    app.run(debug=True)
