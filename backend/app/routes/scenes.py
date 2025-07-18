"""
Scene routes for CRUD operations on scenes.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.scene import Scene
from app.models.chapter import Chapter
from app.models.project import Project
from app.routes.projects import get_current_user

scenes_bp = Blueprint("scenes", __name__)


@scenes_bp.route("/", methods=["POST"])
@jwt_required()
def create_scene():
    """Create a new scene."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401

        data = request.get_json()

        # Validate required fields
        if not data.get("title") or not data.get("chapter_id"):
            return jsonify({"error": "Title and chapter_id are required"}), 400

        # Verify chapter ownership
        chapter = (
            Chapter.query.join(Project)
            .filter(Chapter.id == data["chapter_id"], Project.author_id == user.id)
            .first()
        )

        if not chapter:
            return jsonify({"error": "Chapter not found"}), 404

        # Get next order index
        last_scene = chapter.scenes.order_by(Scene.order_index.desc()).first()
        next_order = (last_scene.order_index + 1) if last_scene else 1

        # Create scene
        scene = Scene(
            title=data["title"],
            content=data.get("content", ""),
            summary=data.get("summary"),
            order_index=data.get("order_index", next_order),
            scene_type=data.get("scene_type", "scene"),
            point_of_view=data.get("point_of_view"),
            location=data.get("location"),
            time_of_day=data.get("time_of_day"),
            notes=data.get("notes"),
            chapter_id=data["chapter_id"],
        )

        # Handle tags
        if data.get("tags"):
            scene.set_tags_list(data["tags"])

        scene.save()

        return (
            jsonify(
                {"message": "Scene created successfully", "scene": scene.to_dict()}
            ),
            201,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@scenes_bp.route("/<scene_id>", methods=["GET"])
@jwt_required()
def get_scene(scene_id):
    """Get a specific scene."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401

        scene = (
            Scene.query.join(Chapter)
            .join(Project)
            .filter(Scene.id == scene_id, Project.author_id == user.id)
            .first()
        )

        if not scene:
            return jsonify({"error": "Scene not found"}), 404

        return jsonify({"scene": scene.to_dict()}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@scenes_bp.route("/<scene_id>", methods=["PUT"])
@jwt_required()
def update_scene(scene_id):
    """Update an existing scene."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401

        scene = (
            Scene.query.join(Chapter)
            .join(Project)
            .filter(Scene.id == scene_id, Project.author_id == user.id)
            .first()
        )

        if not scene:
            return jsonify({"error": "Scene not found"}), 404

        data = request.get_json()

        # Update fields
        updatable_fields = [
            "title",
            "content",
            "summary",
            "order_index",
            "scene_type",
            "point_of_view",
            "location",
            "time_of_day",
            "status",
            "notes",
            "is_draft_mode",
            "draft_content",
        ]

        for field in updatable_fields:
            if field in data:
                setattr(scene, field, data[field])

        # Handle tags
        if "tags" in data:
            scene.set_tags_list(data["tags"])

        db.session.commit()

        return (
            jsonify(
                {"message": "Scene updated successfully", "scene": scene.to_dict()}
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@scenes_bp.route("/<scene_id>", methods=["DELETE"])
@jwt_required()
def delete_scene(scene_id):
    """Delete a scene."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401

        scene = (
            Scene.query.join(Chapter)
            .join(Project)
            .filter(Scene.id == scene_id, Project.author_id == user.id)
            .first()
        )

        if not scene:
            return jsonify({"error": "Scene not found"}), 404

        scene.delete()

        return jsonify({"message": "Scene deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@scenes_bp.route("/<scene_id>/toggle-draft", methods=["POST"])
@jwt_required()
def toggle_draft_mode(scene_id):
    """Toggle draft mode for a scene."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401

        scene = (
            Scene.query.join(Chapter)
            .join(Project)
            .filter(Scene.id == scene_id, Project.author_id == user.id)
            .first()
        )

        if not scene:
            return jsonify({"error": "Scene not found"}), 404

        scene.toggle_draft_mode()

        return (
            jsonify(
                {"message": "Draft mode toggled successfully", "scene": scene.to_dict()}
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
