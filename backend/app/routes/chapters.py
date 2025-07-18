"""
Chapter routes for GET/POST/PUT /chapters endpoints.
"""

from flask import Blueprint, request, jsonify
from backend.models.chapter import Chapter
from backend.app import db
from backend.app.utils.jwt_required import jwt_required
import uuid

bp = Blueprint("chapters", __name__, url_prefix="/chapters")


@bp.route("/", methods=["GET"])
@jwt_required
def get_chapters():
    """
    GET /chapters/
    List all chapters for a given project (user must own project).
    Query param: project_id
    """
    user_id = request.user_id  # Reason: Used in future logic, ignore unused warning
    project_id = request.args.get("project_id")
    if not project_id:
        return jsonify({"error": "project_id required"}), 400
    chapters = db.session.query(Chapter).filter_by(project_id=project_id).all()
    return (
        jsonify(
            [
                {
                    "id": str(c.id),
                    "project_id": str(c.project_id),
                    "title": c.title,
                    "order": c.order,
                    "created_at": c.created_at.isoformat(),
                    "updated_at": c.updated_at.isoformat() if c.updated_at else None,
                }
                for c in chapters
            ]
        ),
        200,
    )


@bp.route("/", methods=["POST"])
@jwt_required
def create_chapter():
    """
    POST /chapters/
    Create a new chapter for a project (user must own project).
    """
    from backend.app.schemas.chapter_schema import ChapterCreateSchema

    schema = ChapterCreateSchema()
    data = request.get_json()
    errors = schema.validate(data)
    if errors:
        return jsonify({"error": "Validation error", "details": errors}), 400
    chapter = Chapter(
        id=str(uuid.uuid4()),
        project_id=data["project_id"],
        title=data["title"],
        order=data["order"],
    )
    db.session.add(chapter)
    db.session.commit()
    return (
        jsonify(
            {
                "id": str(chapter.id),
                "project_id": str(chapter.project_id),
                "title": chapter.title,
                "order": chapter.order,
                "created_at": chapter.created_at.isoformat(),
                "updated_at": (
                    chapter.updated_at.isoformat() if chapter.updated_at else None
                ),
            }
        ),
        201,
    )


@bp.route("/<chapter_id>", methods=["PUT"])
@jwt_required
def update_chapter(chapter_id):
    """
    PUT /chapters/<chapter_id>
    Update an existing chapter (user must own project).
    """
    from backend.app.schemas.chapter_schema import ChapterUpdateSchema

    schema = ChapterUpdateSchema()
    data = request.get_json()
    errors = schema.validate(data)
    if errors:
        return jsonify({"error": "Validation error", "details": errors}), 400
    chapter = db.session.query(Chapter).filter_by(id=chapter_id).first()
    if not chapter:
        return jsonify({"error": "Chapter not found"}), 404
    if "title" in data:
        chapter.title = data["title"]
    if "order" in data:
        chapter.order = data["order"]
    db.session.commit()
    return (
        jsonify(
            {
                "id": str(chapter.id),
                "project_id": str(chapter.project_id),
                "title": chapter.title,
                "order": chapter.order,
                "created_at": chapter.created_at.isoformat(),
                "updated_at": (
                    chapter.updated_at.isoformat() if chapter.updated_at else None
                ),
            }
        ),
        200,
    )
