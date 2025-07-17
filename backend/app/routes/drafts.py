"""
Draft routes for CRUD operations on drafts.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.draft import Draft
from app.models.scene import Scene
from app.models.user import User

drafts_bp = Blueprint("drafts", __name__)


def get_current_user():
    user_id = get_jwt_identity()
    if not user_id:
        return None
    return User.query.get(user_id)


@drafts_bp.route("/", methods=["POST"])
@jwt_required()
def create_draft():
    """Create a new draft for a scene."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401
        data = request.get_json()
        if not data.get("scene_id") or not data.get("content"):
            return jsonify({"error": "scene_id and content are required"}), 400
        scene = Scene.query.get(data["scene_id"])
        if not scene:
            return jsonify({"error": "Scene not found"}), 404
        draft = Draft(
            scene_id=data["scene_id"],
            content=data["content"],
            is_final=data.get("is_final", False),
        )
        db.session.add(draft)
        db.session.commit()
        return (
            jsonify(
                {"message": "Draft created successfully", "draft": draft.to_dict()}
            ),
            201,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@drafts_bp.route("/<draft_id>", methods=["GET"])
@jwt_required()
def get_draft(draft_id):
    """Get a specific draft by ID."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401
        draft = Draft.query.get(draft_id)
        if not draft:
            return jsonify({"error": "Draft not found"}), 404
        return jsonify({"draft": draft.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
