"""
Scene model for chapter scenes.
"""

from app import db
from .base import BaseModel


class Scene(BaseModel):
    __tablename__ = "scenes"
    chapter_id = db.Column(db.String(36), db.ForeignKey("chapters.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    order = db.Column(db.Integer, nullable=False)
    drafts = db.relationship(
        "Draft", backref="scene", cascade="all, delete-orphan", lazy="dynamic"
    )

    # Scene metadata
    scene_type = db.Column(
        db.String(30), default="scene"
    )  # scene, dialogue, action, description
    point_of_view = db.Column(db.String(100))  # Character POV
    location = db.Column(db.String(200))  # Scene setting
    time_of_day = db.Column(db.String(50))  # Morning, afternoon, etc.

    # Scene status and notes
    status = db.Column(
        db.String(20), default="draft"
    )  # draft, in_progress, review, final
    notes = db.Column(db.Text)  # Author notes
    tags = db.Column(db.String(500))  # Comma-separated tags

    # Draft mode
    is_draft_mode = db.Column(db.Boolean, default=False)
    draft_content = db.Column(db.Text)  # Separate draft content

    # Relationships
    chapter_id = db.Column(db.String(36), db.ForeignKey("chapters.id"), nullable=False)
    annotations = db.relationship(
        "Annotation", backref="scene", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Scene {self.title}>"

    def to_dict(self):
        """
        Convert scene instance to dictionary.

        Returns:
            dict: Scene data as dictionary
        """
        data = super().to_dict()
        data.update(
            {
                "title": self.title,
                "content": self.content,
                "summary": self.summary,
                "order_index": self.order_index,
                "scene_type": self.scene_type,
                "point_of_view": self.point_of_view,
                "location": self.location,
                "time_of_day": self.time_of_day,
                "status": self.status,
                "notes": self.notes,
                "tags": self.get_tags_list(),
                "is_draft_mode": self.is_draft_mode,
                "draft_content": self.draft_content,
                "chapter_id": self.chapter_id,
                "word_count": self.get_word_count(),
                "annotation_count": self.annotations.count(),
            }
        )
        return data

    def get_word_count(self):
        """
        Calculate word count for scene content.

        Returns:
            int: Word count for the scene
        """
        content = (
            self.draft_content
            if self.is_draft_mode and self.draft_content
            else self.content
        )
        return len(content.split()) if content else 0

    def get_tags_list(self):
        """
        Get tags as a list instead of comma-separated string.

        Returns:
            list: List of tags
        """
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(",") if tag.strip()]

    def set_tags_list(self, tags_list):
        """
        Set tags from a list.

        Args:
            tags_list (list): List of tag strings
        """
        self.tags = ", ".join(tags_list) if tags_list else None

    def toggle_draft_mode(self):
        """
        Toggle between draft mode and normal mode.
        """
        self.is_draft_mode = not self.is_draft_mode
        db.session.commit()

    def publish_draft(self):
        """
        Move draft content to main content and exit draft mode.
        """
        if self.is_draft_mode and self.draft_content:
            self.content = self.draft_content
            self.draft_content = None
            self.is_draft_mode = False
            db.session.commit()
