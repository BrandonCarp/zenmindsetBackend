from ..app import db  # Import db from app
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(128), nullable=False)  # Increased length for hashed passwords
    email = db.Column(db.String(100), nullable=False, unique=True)
    profile_picture = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(datetime.timezone.utc))
    last_login = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(20), default='user')
    bio = db.Column(db.Text, nullable=True)

    def __repr__(self) -> str:
        return f"User {self.id}, user_name={self.user_name}, email={self.email}"
