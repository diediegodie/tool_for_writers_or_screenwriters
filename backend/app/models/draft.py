"""
Draft model for scene drafts.
"""

from app import db
from .base import BaseModel


class Draft(BaseModel):
    __tablename__ = "drafts"
    scene_id = db.Column(db.String(36), db.ForeignKey("scenes.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_final = db.Column(db.Boolean, default=False)
