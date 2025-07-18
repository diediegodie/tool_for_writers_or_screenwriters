"""
ExportMetadata model for tracking export history.
"""

from sqlalchemy import DateTime, String
import uuid
from datetime import datetime
from backend.app import db


class ExportMetadata(db.Model):
    """
    ExportMetadata model for tracking export history.
    """

    __tablename__ = "exports"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), nullable=False)
    format = db.Column(db.String(8), nullable=False)  # 'pdf' or 'docx'
    file_name = db.Column(db.String(128), nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)
