"""
Annotation model for highlights with context in a draft.
"""

from sqlalchemy import String, DateTime, Text
import uuid
from datetime import datetime
from backend.app import db


class Annotation(db.Model):
    """
    Annotation model for highlights with context in a draft.
    """

    __tablename__ = "annotations"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    draft_id = db.Column(db.String(36), db.ForeignKey("drafts.id"), nullable=False)
    context = db.Column(Text)
    highlight = db.Column(Text)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
