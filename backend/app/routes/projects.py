def get_owned_project_or_404(user_id, project_id):
    project = Project.query.filter_by(id=project_id, user_id=user_id).first()
    if not project:
        return None, (
            jsonify({"error": "Forbidden: You do not have access to this project."}),
            403,
        )
    return project, None


"""
Project routes for CRUD operations on writing projects.
"""

from flask import Blueprint, request, jsonify
from app import db
from app.models.project import Project
from app.models.user import User

from flask_jwt_extended import jwt_required, get_jwt_identity

projects_bp = Blueprint("projects", __name__)


def get_current_user():
    """Helper to get current user from JWT identity."""
    user_id = get_jwt_identity()
    if not user_id:
        return None
    return User.query.get(user_id)


@projects_bp.route("/", methods=["GET"])
@jwt_required()
def get_projects():
    """Get all projects for the current user."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401

        projects = user.projects.all()
        return jsonify({"projects": [project.to_dict() for project in projects]}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@projects_bp.route("/", methods=["POST"])
@jwt_required()
def create_project():
    """Create a new project."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401

        data = request.get_json()

        # Validate required fields
        if not data.get("title"):
            return jsonify({"error": "Title is required"}), 400

        # Create project
        project = Project(
            title=data["title"],
            description=data.get("description"),
            genre=data.get("genre"),
            project_type=data.get("project_type", "book"),
            word_count_goal=data.get("word_count_goal"),
            author_id=user.id,
        )
        project.save()

        return (
            jsonify(
                {
                    "message": "Project created successfully",
                    "project": project.to_dict(),
                }
            ),
            201,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@projects_bp.route("/<project_id>", methods=["GET"])
@jwt_required()
def get_project(project_id):
    """Get a specific project with its chapters."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401

        project = Project.query.filter_by(id=project_id, author_id=user.id).first()
        if not project:
            return jsonify({"error": "Project not found"}), 404

        # Include chapters in response
        project_data = project.to_dict()
        project_data["chapters"] = [
            chapter.to_dict() for chapter in project.chapters.all()
        ]

        return jsonify({"project": project_data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@projects_bp.route("/<project_id>", methods=["PUT"])
@jwt_required()
def update_project(project_id):
    """Update an existing project."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401

        project = Project.query.filter_by(id=project_id, author_id=user.id).first()
        if not project:
            return jsonify({"error": "Project not found"}), 404

        data = request.get_json()

        # Update fields
        if "title" in data:
            project.title = data["title"]
        if "description" in data:
            project.description = data["description"]
        if "genre" in data:
            project.genre = data["genre"]
        if "project_type" in data:
            project.project_type = data["project_type"]
        if "word_count_goal" in data:
            project.word_count_goal = data["word_count_goal"]
        if "status" in data:
            project.status = data["status"]

        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Project updated successfully",
                    "project": project.to_dict(),
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@projects_bp.route("/<project_id>", methods=["DELETE"])
@jwt_required()
def delete_project(project_id):
    """Delete a project."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401

        project = Project.query.filter_by(id=project_id, author_id=user.id).first()
        if not project:
            return jsonify({"error": "Project not found"}), 404

        project.delete()

        return jsonify({"message": "Project deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
