"""
Project model for writing projects.
"""

from app import db
from .base import BaseModel


class Project(BaseModel):
    __tablename__ = "projects"
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    chapters = db.relationship(
        "Chapter", backref="project", cascade="all, delete-orphan", lazy="dynamic"
    )
