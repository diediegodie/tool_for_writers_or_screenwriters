"""
Export routes for generating DOCX and PDF documents.
"""

from flask import Blueprint, request, jsonify
from app.models.project import Project
from app.routes.projects import get_current_user_from_token

exports_bp = Blueprint("exports", __name__)


@exports_bp.route("/<project_id>", methods=["POST"])
def export_project(project_id):
    """Export a project to DOCX or PDF format."""
    try:
        user = get_current_user_from_token()
        if not user:
            return jsonify({"error": "Authentication required"}), 401

        # Verify project ownership
        project = Project.query.filter_by(id=project_id, author_id=user.id).first()
        if not project:
            return jsonify({"error": "Project not found"}), 404

        data = request.get_json()
        export_type = data.get("export_type", "docx")

        if export_type not in ["docx", "pdf"]:
            return jsonify({"error": 'Invalid export type. Use "docx" or "pdf"'}), 400

        # TODO: Implement actual export functionality
        # This is a placeholder response
        return (
            jsonify(
                {
                    "message": f"Export functionality will be implemented in Phase 2.6",
                    "export_type": export_type,
                    "project_id": project_id,
                    "project_title": project.title,
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
