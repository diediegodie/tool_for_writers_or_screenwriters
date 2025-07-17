"""
Annotation model for draft annotations.
"""

from app import db
from .base import BaseModel


class Annotation(BaseModel):
    __tablename__ = "annotations"
    draft_id = db.Column(db.String(36), db.ForeignKey("drafts.id"), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    start_offset = db.Column(db.Integer)
    end_offset = db.Column(db.Integer)

    # Position information
    start_position = db.Column(db.Integer, nullable=False)
    end_position = db.Column(db.Integer, nullable=False)

    # Status
    is_resolved = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(10), default="medium")  # low, medium, high

    # Relationships
    scene_id = db.Column(db.String(36), db.ForeignKey("scenes.id"), nullable=False)

    def __repr__(self):
        return f"<Annotation {self.annotation_type}: {self.highlighted_text[:50]}...>"

    def to_dict(self):
        """
        Convert annotation instance to dictionary.

        Returns:
            dict: Annotation data as dictionary
        """
        data = super().to_dict()
        data.update(
            {
                "highlighted_text": self.highlighted_text,
                "note": self.note,
                "annotation_type": self.annotation_type,
                "start_position": self.start_position,
                "end_position": self.end_position,
                "is_resolved": self.is_resolved,
                "priority": self.priority,
                "scene_id": self.scene_id,
            }
        )
        return data
