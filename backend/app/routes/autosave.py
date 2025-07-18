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
    # Reason: Server-side deduplication to prevent duplicate autosaves within 30 seconds
    from datetime import datetime, timedelta

    user_id = None
    # Get user identity from JWT
    from flask_jwt_extended import get_jwt_identity

    user_id = get_jwt_identity()
    # Build query for latest autosave
    query = AutosaveVersion.query
    if data.get("scene_id"):
        query = query.filter_by(scene_id=data["scene_id"])
    if data.get("draft_id"):
        query = query.filter_by(draft_id=data["draft_id"])
    # If user_id is tracked in AutosaveVersion, filter by user_id (not present in current model)
    # Get latest autosave
    latest = query.order_by(AutosaveVersion.saved_at.desc()).first()
    now = datetime.utcnow()

    def seconds_since(ts):
        if not ts:
            return None
        return (now - ts).total_seconds()

    if (
        latest
        and latest.content == data["content"]
        and seconds_since(latest.saved_at) is not None
        and seconds_since(latest.saved_at) < 30
    ):
        # Reason: Duplicate snapshot within 30 seconds, skip saving
        return jsonify(autosave_schema.dump(latest)), 200
    autosave = AutosaveVersion(
        scene_id=data.get("scene_id"),
        draft_id=data.get("draft_id"),
        content=data["content"],
    )
    db.session.add(autosave)
    db.session.commit()
    return jsonify(autosave_schema.dump(autosave)), 201
