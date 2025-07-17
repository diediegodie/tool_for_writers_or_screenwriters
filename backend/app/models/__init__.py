"""
Base model class with common fields and utilities.
All models inherit from this base class.
"""

from datetime import datetime
from app import db
import uuid


class BaseModel(db.Model):
    """
    Abstract base model with common fields.
    Provides id, created_at, updated_at for all models.
    """

    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def to_dict(self):
        """
        Convert model instance to dictionary.

        Returns:
            dict: Model data as dictionary
        """
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def save(self):
        """Save the model instance to database."""
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """Delete the model instance from database."""
        db.session.delete(self)
        db.session.commit()
        return True
