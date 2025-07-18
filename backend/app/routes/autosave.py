"""
Autosave route for POST /autosave
"""

from flask import Blueprint, request, jsonify
from backend.models.autosave_version import AutosaveVersion
from backend.app import db
from backend.app.schemas.autosave_version_schema import AutosaveVersionSchema
from flask_jwt_extended import jwt_required

bp = Blueprint("autosave", __name__, url_prefix="/autosave")
autosave_schema = AutosaveVersionSchema()


@bp.route("/", methods=["POST"])
@jwt_required()
def autosave():
    """Create a new autosave snapshot for a scene or draft."""
    data = request.get_json()
    errors = autosave_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    if not data.get("scene_id") and not data.get("draft_id"):
        return jsonify({"error": "scene_id or draft_id required"}), 400
    autosave = AutosaveVersion(
        scene_id=data.get("scene_id"),
        draft_id=data.get("draft_id"),
        content=data["content"],
    )
    db.session.add(autosave)
    db.session.commit()
    return jsonify(autosave_schema.dump(autosave)), 201
