"""
Scene model for scenes grouped within chapters.
"""

from sqlalchemy import String, Integer, DateTime, Text
import uuid
from datetime import datetime
from backend.app import db


class Scene(db.Model):
    """
    Scene model for scenes grouped within chapters.
    """

    __tablename__ = "scenes"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    chapter_id = db.Column(db.String(36), db.ForeignKey("chapters.id"), nullable=False)
    title = db.Column(String(200), nullable=False)
    content = db.Column(Text)
    order = db.Column(Integer, nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
