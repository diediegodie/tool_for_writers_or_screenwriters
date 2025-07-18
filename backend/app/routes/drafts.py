"""
Draft routes for GET/POST /drafts/
"""

from flask import Blueprint, request, jsonify
from backend.models.draft import Draft
from backend.app import db
from backend.app.schemas.draft_schema import DraftSchema
from flask_jwt_extended import jwt_required

bp = Blueprint("drafts", __name__, url_prefix="/drafts")

draft_schema = DraftSchema()
drafts_schema = DraftSchema(many=True)


@bp.route("/", methods=["GET"])
@jwt_required()
def get_drafts():
    """Get all drafts."""
    drafts = Draft.query.all()
    return jsonify(drafts_schema.dump(drafts)), 200


@bp.route("/", methods=["POST"])
@jwt_required()
def create_draft():
    """Create a new draft."""
    data = request.get_json()
    errors = draft_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    draft = Draft(scene_id=data["scene_id"], content=data.get("content", ""))
    db.session.add(draft)
    db.session.commit()
    return jsonify(draft_schema.dump(draft)), 201
