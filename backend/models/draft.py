"""
Draft model for temporary versions of scenes.
"""

from sqlalchemy import DateTime, Text
import uuid
from datetime import datetime
from backend.app import db


class Draft(db.Model):
    """
    Draft model for temporary versions of scenes.
    """

    __tablename__ = "drafts"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    scene_id = db.Column(db.String(36), db.ForeignKey("scenes.id"), nullable=False)
    content = db.Column(Text)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
