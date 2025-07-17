"""
Chapter model for project chapters.
"""

from app import db
from .base import BaseModel


class Chapter(BaseModel):
    __tablename__ = "chapters"
    project_id = db.Column(db.String(36), db.ForeignKey("projects.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    scenes = db.relationship(
        "Scene", backref="chapter", cascade="all, delete-orphan", lazy="dynamic"
    )
    is_active = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)  # Private notes for the author

    # Relationships
    project_id = db.Column(db.String(36), db.ForeignKey("projects.id"), nullable=False)
    scenes = db.relationship(
        "Scene",
        backref="chapter",
        lazy="dynamic",
        cascade="all, delete-orphan",
        order_by="Scene.order_index",
    )

    def __repr__(self):
        return f"<Chapter {self.title}>"

    def to_dict(self):
        """
        Convert chapter instance to dictionary.

        Returns:
            dict: Chapter data as dictionary
        """
        data = super().to_dict()
        data.update(
            {
                "title": self.title,
                "description": self.description,
                "order_index": self.order_index,
                "is_active": self.is_active,
                "notes": self.notes,
                "project_id": self.project_id,
                "scene_count": self.scenes.count(),
                "word_count": self.get_word_count(),
            }
        )
        return data

    def get_word_count(self):
        """
        Calculate word count for all scenes in this chapter.

        Returns:
            int: Total word count for the chapter
        """
        total = 0
        for scene in self.scenes:
            if scene.content:
                total += len(scene.content.split())
        return total

    def get_scene_by_order(self, order_index):
        """
        Get scene by its order index.

        Args:
            order_index (int): Order index of the scene

        Returns:
            Scene: Scene instance or None
        """
        return self.scenes.filter_by(order_index=order_index).first()

    def reorder_scenes(self):
        """
        Reorder scenes to ensure sequential order_index values.
        Useful after deleting scenes or reordering.
        """
        scenes = self.scenes.order_by("order_index").all()
        for i, scene in enumerate(scenes):
            scene.order_index = i + 1
        db.session.commit()
