"""
Export model for history of user exports.
"""

from sqlalchemy import DateTime, String
from datetime import datetime
import uuid
from backend.app import db


class Export(db.Model):
    """
    Export model for history of user exports.
    """

    __tablename__ = "exports"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    project_id = db.Column(db.String(36), db.ForeignKey("projects.id"), nullable=False)
    export_type = db.Column(String(10), nullable=False)  # docx or pdf
    file_path = db.Column(String(300), nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)
