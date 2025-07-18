"""
Export model for history of user exports.
"""

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()


class Export(Base):
    """
    Export model for history of user exports.
    """

    __tablename__ = "exports"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    export_type = Column(String(10), nullable=False)  # docx or pdf
    file_path = Column(String(300), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
