"""
AutosaveVersion model for autosave snapshots.
"""

from app import db
from .base import BaseModel


class AutosaveVersion(BaseModel):
    __tablename__ = "autosave_versions"
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    project_id = db.Column(db.String(36), db.ForeignKey("projects.id"), nullable=False)
    data = db.Column(db.JSON, nullable=False)
    saved_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    scene_id = db.Column(
        db.String(36)
    )  # Optional: specific scene that was being edited
    total_word_count = db.Column(db.Integer, default=0)

    # Relationships
    project_id = db.Column(db.String(36), db.ForeignKey("projects.id"), nullable=False)

    def __repr__(self):
        return f"<AutosaveVersion {self.version_number} for Project {self.project_id}>"

    def to_dict(self):
        """
        Convert autosave version instance to dictionary.

        Returns:
            dict: Autosave version data as dictionary
        """
        data = super().to_dict()
        data.update(
            {
                "version_number": self.version_number,
                "content_snapshot": self.content_snapshot,
                "change_summary": self.change_summary,
                "scene_id": self.scene_id,
                "total_word_count": self.total_word_count,
                "project_id": self.project_id,
            }
        )
        return data

    @staticmethod
    def get_latest_version(project_id):
        """
        Get the latest autosave version for a project.

        Args:
            project_id (str): Project ID

        Returns:
            AutosaveVersion: Latest version or None
        """
        return (
            AutosaveVersion.query.filter_by(project_id=project_id)
            .order_by(AutosaveVersion.version_number.desc())
            .first()
        )

    @staticmethod
    def cleanup_old_versions(project_id, max_versions=50):
        """
        Remove old autosave versions, keeping only the most recent ones.

        Args:
            project_id (str): Project ID
            max_versions (int): Maximum number of versions to keep
        """
        versions = (
            AutosaveVersion.query.filter_by(project_id=project_id)
            .order_by(AutosaveVersion.version_number.desc())
            .all()
        )

        if len(versions) > max_versions:
            versions_to_delete = versions[max_versions:]
            for version in versions_to_delete:
                db.session.delete(version)
            db.session.commit()
