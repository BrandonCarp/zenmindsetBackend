# models/item.py
from ..app import db  # Import db from app
from datetime import datetime

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(datetime.timezone.utc))

    def __repr__(self) -> str:
        return f"Item {self.id}"
