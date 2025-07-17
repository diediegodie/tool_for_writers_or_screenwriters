"""
Export model for project exports.
"""

from app import db
from .base import BaseModel


class Export(BaseModel):
    __tablename__ = "exports"
    project_id = db.Column(db.String(36), db.ForeignKey("projects.id"), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    export_type = db.Column(db.String(10), nullable=False)  # 'pdf' or 'docx'
    file_path = db.Column(db.String(255), nullable=False)
    chapter_range_start = db.Column(db.Integer)  # Optional: export specific chapters
    chapter_range_end = db.Column(db.Integer)

    # Status and metadata
    status = db.Column(db.String(20), default="pending")  # pending, completed, failed
    error_message = db.Column(db.Text)
    download_count = db.Column(db.Integer, default=0)

    # Relationships
    project_id = db.Column(db.String(36), db.ForeignKey("projects.id"), nullable=False)

    def __repr__(self):
        return f"<Export {self.export_type}: {self.filename}>"

    def to_dict(self):
        """
        Convert export instance to dictionary.

        Returns:
            dict: Export data as dictionary
        """
        data = super().to_dict()
        data.update(
            {
                "export_type": self.export_type,
                "filename": self.filename,
                "file_size": self.file_size,
                "include_notes": self.include_notes,
                "include_annotations": self.include_annotations,
                "chapter_range_start": self.chapter_range_start,
                "chapter_range_end": self.chapter_range_end,
                "status": self.status,
                "error_message": self.error_message,
                "download_count": self.download_count,
                "project_id": self.project_id,
            }
        )
        return data

    def increment_download_count(self):
        """Increment the download counter."""
        self.download_count += 1
        db.session.commit()
