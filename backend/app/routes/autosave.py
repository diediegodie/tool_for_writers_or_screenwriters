"""
Autosave routes for automatic content backup.
"""

from flask import Blueprint, request, jsonify
from app.models.autosave import AutosaveVersion
from app.models.project import Project
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User


def get_current_user():
    user_id = get_jwt_identity()
    if not user_id:
        return None
    return User.query.get(user_id)


autosave_bp = Blueprint("autosave", __name__)


@autosave_bp.route("/", methods=["POST"])
@jwt_required()
def create_autosave():
    """Create an autosave version for a project."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401

        data = request.get_json()

        # Validate required fields
        if not data.get("project_id") or not data.get("content_snapshot"):
            return (
                jsonify({"error": "project_id and content_snapshot are required"}),
                400,
            )

        # Verify project ownership
        project = Project.query.filter_by(
            id=data["project_id"], author_id=user.id
        ).first()
        if not project:
            return jsonify({"error": "Project not found"}), 404

        # Get next version number
        latest_version = AutosaveVersion.get_latest_version(data["project_id"])
        next_version = (latest_version.version_number + 1) if latest_version else 1

        # Create autosave version
        autosave = AutosaveVersion(
            version_number=next_version,
            content_snapshot=data["content_snapshot"],
            change_summary=data.get("change_summary"),
            scene_id=data.get("scene_id"),
            total_word_count=data.get("total_word_count", 0),
            project_id=data["project_id"],
        )
        autosave.save()

        # Cleanup old versions
        AutosaveVersion.cleanup_old_versions(data["project_id"])

        return (
            jsonify(
                {
                    "message": "Autosave created successfully",
                    "autosave": autosave.to_dict(),
                }
            ),
            201,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@autosave_bp.route("/<project_id>/versions", methods=["GET"])
@jwt_required()
def get_autosave_versions(project_id):
    """Get autosave versions for a project."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401

        # Verify project ownership
        project = Project.query.filter_by(id=project_id, author_id=user.id).first()
        if not project:
            return jsonify({"error": "Project not found"}), 404

        # Get recent versions (limit to last 10)
        versions = (
            AutosaveVersion.query.filter_by(project_id=project_id)
            .order_by(AutosaveVersion.version_number.desc())
            .limit(10)
            .all()
        )

        return jsonify({"versions": [version.to_dict() for version in versions]}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
