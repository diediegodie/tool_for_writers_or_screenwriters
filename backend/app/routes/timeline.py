"""
Timeline route for retrieving a project's timeline (ordered scenes and chapters).
"""

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.project import Project
from app.models.chapter import Chapter
from app.models.scene import Scene
from app.models.user import User

timeline_bp = Blueprint("timeline", __name__)


def get_current_user():
    user_id = get_jwt_identity()
    if not user_id:
        return None
    return User.query.get(user_id)


@timeline_bp.route("/<project_id>", methods=["GET"])
@jwt_required()
def get_timeline(project_id):
    """Get the timeline (ordered chapters and scenes) for a project."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401
        project = Project.query.filter_by(id=project_id, author_id=user.id).first()
        if not project:
            return jsonify({"error": "Project not found"}), 404
        chapters = (
            Chapter.query.filter_by(project_id=project_id)
            .order_by(Chapter.order.asc())
            .all()
        )
        timeline = []
        for chapter in chapters:
            scenes = (
                Scene.query.filter_by(chapter_id=chapter.id)
                .order_by(Scene.order.asc())
                .all()
            )
            timeline.append(
                {
                    "chapter": chapter.to_dict(),
                    "scenes": [scene.to_dict() for scene in scenes],
                }
            )
        return jsonify({"timeline": timeline}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
