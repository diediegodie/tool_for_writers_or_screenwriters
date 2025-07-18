"""
Project routes for GET/POST/PUT /projects endpoints.
"""

from flask import Blueprint, request, jsonify
from backend.models.project import Project
from backend.app import db
from backend.app.utils.jwt_required import jwt_required
from backend.app.services.auth_service import AuthService
import uuid

bp = Blueprint("projects", __name__, url_prefix="/projects")


@bp.route("/", methods=["GET"])
@jwt_required
def get_projects():
    """
    GET /projects/
    List all projects for the authenticated user.
    """
    user_id = request.user_id
    projects = db.session.query(Project).filter_by(user_id=user_id).all()
    return (
        jsonify(
            [
                {
                    "id": str(p.id),
                    "title": p.title,
                    "description": p.description,
                    "created_at": p.created_at.isoformat(),
                    "updated_at": p.updated_at.isoformat() if p.updated_at else None,
                }
                for p in projects
            ]
        ),
        200,
    )


@bp.route("/", methods=["POST"])
@jwt_required
def create_project():
    """
    POST /projects/
    Create a new project for the authenticated user.
    """
    from backend.app.schemas.project_schema import ProjectCreateSchema

    schema = ProjectCreateSchema()
    data = request.get_json()
    errors = schema.validate(data)
    if errors:
        return jsonify({"error": "Validation error", "details": errors}), 400
    user_id = request.user_id
    project = Project(
        id=str(uuid.uuid4()),
        user_id=user_id,
        title=data["title"],
        description=data.get("description", ""),
    )
    db.session.add(project)
    db.session.commit()
    return (
        jsonify(
            {
                "id": str(project.id),
                "title": project.title,
                "description": project.description,
                "created_at": project.created_at.isoformat(),
                "updated_at": (
                    project.updated_at.isoformat() if project.updated_at else None
                ),
            }
        ),
        201,
    )


@bp.route("/<project_id>", methods=["PUT"])
@jwt_required
def update_project(project_id):
    """
    PUT /projects/<project_id>
    Update an existing project for the authenticated user.
    """
    from backend.app.schemas.project_schema import ProjectUpdateSchema

    schema = ProjectUpdateSchema()
    data = request.get_json()
    errors = schema.validate(data)
    if errors:
        return jsonify({"error": "Validation error", "details": errors}), 400
    user_id = request.user_id
    project = (
        db.session.query(Project).filter_by(id=project_id, user_id=user_id).first()
    )
    if not project:
        return jsonify({"error": "Project not found"}), 404
    if "title" in data:
        project.title = data["title"]
    if "description" in data:
        project.description = data["description"]
    db.session.commit()
    return (
        jsonify(
            {
                "id": str(project.id),
                "title": project.title,
                "description": project.description,
                "created_at": project.created_at.isoformat(),
                "updated_at": (
                    project.updated_at.isoformat() if project.updated_at else None
                ),
            }
        ),
        200,
    )
