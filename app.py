from flask import Flask   
from config import Config 
from extensions import db
from routes.user_routes import user_bp  

# Initialize the Flask app
app = Flask(__name__)


app.config.from_object(Config)


db.init_app(app)


app.register_blueprint(user_bp, url_prefix='/api/users')


if __name__ == "__main__":
   
    with app.app_context():
        db.create_all()  # Creates tables based on models if they don't already exist
    app.run(debug=True) 

## API Endpoints

# - `POST /api/users/register`: Register a new user.
# - Add other user-related endpoints under this blueprint as needed.
