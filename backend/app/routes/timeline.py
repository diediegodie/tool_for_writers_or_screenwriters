"""
Timeline route for GET /timeline/<project_id>
"""

from flask import Blueprint, jsonify
from backend.models.project import Project
from backend.models.chapter import Chapter
from backend.models.scene import Scene
from flask_jwt_extended import jwt_required

bp = Blueprint("timeline", __name__, url_prefix="/timeline")


@bp.route("/<project_id>", methods=["GET"])
@jwt_required()
def get_timeline(project_id):
    """Get timeline for a project: chapters and scenes ordered."""
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return jsonify({"error": "Project not found"}), 404
    chapters = (
        Chapter.query.filter_by(project_id=project_id)
        .order_by(Chapter.created_at)
        .all()
    )
    timeline = []
    for chapter in chapters:
        scenes = (
            Scene.query.filter_by(chapter_id=chapter.id)
            .order_by(Scene.created_at)
            .all()
        )
        timeline.append(
            {
                "chapter_id": chapter.id,
                "chapter_title": getattr(chapter, "title", ""),
                "scenes": [
                    {
                        "scene_id": scene.id,
                        "scene_title": getattr(scene, "title", ""),
                        "created_at": scene.created_at.isoformat(),
                    }
                    for scene in scenes
                ],
            }
        )
    return (
        jsonify(
            {
                "project_id": project.id,
                "project_title": getattr(project, "title", ""),
                "timeline": timeline,
            }
        ),
        200,
    )
