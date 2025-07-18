"""
AutosaveVersion model for time-based snapshots of scene or draft content.
"""

from sqlalchemy import Column, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()


class AutosaveVersion(Base):
    """
    AutosaveVersion model for time-based snapshots of scene or draft content.
    """

    __tablename__ = "autosave_versions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scene_id = Column(UUID(as_uuid=True), ForeignKey("scenes.id"), nullable=True)
    draft_id = Column(UUID(as_uuid=True), ForeignKey("drafts.id"), nullable=True)
    content = Column(Text)
    saved_at = Column(DateTime, default=datetime.utcnow)
