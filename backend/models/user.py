"""
User model for authentication info.
"""

from sqlalchemy import String, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from backend.app import db


class User(db.Model):
    """
    User model for authentication info (JWT-based, hashed passwords).
    """

    __tablename__ = "users"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(String(120), unique=True, nullable=False)
    password_hash = db.Column(String(128), nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
