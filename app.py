# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from routes.item_routes import item_bp  # Import the item routes

# Initialize the app and database
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Register blueprints
app.register_blueprint(item_bp, url_prefix='/api/items')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables
    app.run(debug=True)


## API Endpoints

# - `POST /api/items`: Create a new item.
# - `GET /api/items`: Retrieve all items.