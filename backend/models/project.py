"""
Project model for books/scripts created by a user.
"""

from sqlalchemy import String, DateTime
import uuid
from datetime import datetime
from backend.app import db


class Project(db.Model):
    """
    Project model for books/scripts created by a user.
    """

    __tablename__ = "projects"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    title = db.Column(String(200), nullable=False)
    description = db.Column(String(500))
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
