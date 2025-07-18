"""
Chapter model for top-level structure in a project.
"""

from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from backend.app import db


class Chapter(db.Model):
    """
    Chapter model for top-level structure in a project.
    """

    __tablename__ = "chapters"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = db.Column(db.String(36), db.ForeignKey("projects.id"), nullable=False)
    title = db.Column(String(200), nullable=False)
    order = db.Column(Integer, nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
