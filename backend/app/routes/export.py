"""
Export route for POST /export/<project_id>
"""

from flask import Blueprint, request, jsonify
from backend.models.export import Export
from backend.models.project import Project
from backend.app import db
from backend.app.schemas.export_schema import ExportSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from datetime import datetime
from backend.models.user import User  # Reason: Used for future permission checks

bp = Blueprint("export", __name__, url_prefix="/export")
export_schema = ExportSchema()


@bp.route("/<project_id>", methods=["POST"])
@jwt_required()
def export_project(project_id):
    """Export project to docx or pdf and save export metadata."""
    data = request.get_json()
    export_type = data.get("export_type")
    if export_type not in ["docx", "pdf"]:
        return jsonify({"error": "Invalid export_type. Must be 'docx' or 'pdf'."}), 400
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return jsonify({"error": "Project not found."}), 404
    user_id = get_jwt_identity()
    # Reason: Simulate export file creation
    file_name = f"export_{project_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.{export_type}"
    file_path = os.path.join("/tmp", file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"Exported {export_type} for project {project_id}")
    export = Export(
        user_id=user_id,
        project_id=project_id,
        export_type=export_type,
        file_path=file_path,
    )
    db.session.add(export)
    db.session.commit()
    return jsonify(export_schema.dump(export)), 201
