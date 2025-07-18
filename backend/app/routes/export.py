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
    # Reason: Generate real DOCX or PDF file
    import io

    file_name = f"export_{project_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.{export_type}"
    file_stream = io.BytesIO()
    content = getattr(project, "title", "")
    if export_type == "docx":
        from docx import Document

        doc = Document()
        doc.add_paragraph(content)
        doc.save(file_stream)
    elif export_type == "pdf":
        from reportlab.pdfgen import canvas

        c = canvas.Canvas(file_stream)
        c.drawString(100, 750, content)
        c.save()
    else:
        return jsonify({"error": "Invalid export_type. Must be 'docx' or 'pdf'."}), 400
    file_stream.seek(0)
    # Save metadata
    export = Export(
        user_id=user_id,
        project_id=project_id,
        export_type=export_type,
        file_path=file_name,
    )
    db.session.add(export)
    db.session.commit()
    from flask import send_file

    return send_file(
        file_stream,
        as_attachment=True,
        download_name=file_name,
        mimetype=(
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            if export_type == "docx"
            else "application/pdf"
        ),
    )
