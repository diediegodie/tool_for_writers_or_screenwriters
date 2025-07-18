"""
AutosaveVersion model for time-based snapshots of scene or draft content.
"""

from sqlalchemy import DateTime, Text
import uuid
from datetime import datetime
from backend.app import db


class AutosaveVersion(db.Model):
    """
    AutosaveVersion model for time-based snapshots of scene or draft content.
    """

    __tablename__ = "autosave_versions"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    scene_id = db.Column(db.String(36), db.ForeignKey("scenes.id"), nullable=True)
    draft_id = db.Column(db.String(36), db.ForeignKey("drafts.id"), nullable=True)
    content = db.Column(Text)
    saved_at = db.Column(DateTime, default=datetime.utcnow)
