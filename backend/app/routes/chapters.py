"""
Chapter routes for CRUD operations on chapters.
"""

from flask import Blueprint, request, jsonify
from app import db
from app.models.chapter import Chapter
from app.models.project import Project

from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User


def get_current_user():
    user_id = get_jwt_identity()
    if not user_id:
        return None
    return User.query.get(user_id)


from flask import Blueprint, request, jsonify
from app import db
from app.models.chapter import Chapter
from app.models.project import Project

from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User


def get_owned_project_or_404(user_id, project_id):
    project = Project.query.filter_by(id=project_id, user_id=user_id).first()
    if not project:
        return None, (
            jsonify({"error": "Forbidden: You do not have access to this project."}),
            403,
        )
    return project, None


def get_owned_chapter_or_404(user_id, chapter_id):
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        return None, (jsonify({"error": "Chapter not found."}), 404)
    project, err = get_owned_project_or_404(user_id, chapter.project_id)
    if err:
        return None, err
    return chapter, None


def get_current_user():
    user_id = get_jwt_identity()
    if not user_id:
        return None
    return User.query.get(user_id)


chapters_bp = Blueprint("chapters", __name__)


@chapters_bp.route("/", methods=["POST"])
@jwt_required()
def create_chapter():
    """Create a new chapter."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401

        data = request.get_json()

        # Validate required fields
        if not data.get("title") or not data.get("project_id"):
            return jsonify({"error": "Title and project_id are required"}), 400

        # Verify project ownership
        project = Project.query.filter_by(
            id=data["project_id"], author_id=user.id
        ).first()
        if not project:
            return jsonify({"error": "Project not found"}), 404

        # Get next order index
        last_chapter = project.chapters.order_by(Chapter.order_index.desc()).first()
        next_order = (last_chapter.order_index + 1) if last_chapter else 1

        # Create chapter
        chapter = Chapter(
            title=data["title"],
            description=data.get("description"),
            order_index=data.get("order_index", next_order),
            notes=data.get("notes"),
            project_id=data["project_id"],
        )
        chapter.save()

        return (
            jsonify(
                {
                    "message": "Chapter created successfully",
                    "chapter": chapter.to_dict(),
                }
            ),
            201,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@chapters_bp.route("/<chapter_id>", methods=["GET"])
@jwt_required()
def get_chapter(chapter_id):
    """Get a specific chapter with its scenes."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401
        chapter, err = get_owned_chapter_or_404(user.id, chapter_id)
        if err:
            return err
        chapter_data = chapter.to_dict()
        chapter_data["scenes"] = [scene.to_dict() for scene in chapter.scenes.all()]
        return jsonify({"chapter": chapter_data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@chapters_bp.route("/<chapter_id>", methods=["PUT"])
@jwt_required()
def update_chapter(chapter_id):
    """Update an existing chapter."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401
        chapter, err = get_owned_chapter_or_404(user.id, chapter_id)
        if err:
            return err
        data = request.get_json()
        if "title" in data:
            chapter.title = data["title"]
        if "description" in data:
            chapter.description = data["description"]
        if "order" in data:
            chapter.order = data["order"]
        if "notes" in data:
            chapter.notes = data["notes"]
        if "is_active" in data:
            chapter.is_active = data["is_active"]
        db.session.commit()
        return (
            jsonify(
                {
                    "message": "Chapter updated successfully",
                    "chapter": chapter.to_dict(),
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@chapters_bp.route("/<chapter_id>", methods=["DELETE"])
@jwt_required()
def delete_chapter(chapter_id):
    """Delete a chapter."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401
        chapter, err = get_owned_chapter_or_404(user.id, chapter_id)
        if err:
            return err
        db.session.delete(chapter)
        db.session.commit()
        return jsonify({"message": "Chapter deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
