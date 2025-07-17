"""
Annotation routes for CRUD operations on annotations.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.annotation import Annotation
from app.models.draft import Draft
from app.models.user import User

annotations_bp = Blueprint("annotations", __name__)


def get_current_user():
    user_id = get_jwt_identity()
    if not user_id:
        return None
    return User.query.get(user_id)


@annotations_bp.route("/", methods=["POST"])
@jwt_required()
def create_annotation():
    """Create a new annotation for a draft."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401
        data = request.get_json()
        if not data.get("draft_id") or not data.get("content"):
            return jsonify({"error": "draft_id and content are required"}), 400
        draft = Draft.query.get(data["draft_id"])
        if not draft:
            return jsonify({"error": "Draft not found"}), 404
        annotation = Annotation(
            draft_id=data["draft_id"],
            user_id=user.id,
            content=data["content"],
            start_offset=data.get("start_offset"),
            end_offset=data.get("end_offset"),
        )
        db.session.add(annotation)
        db.session.commit()
        return (
            jsonify(
                {
                    "message": "Annotation created successfully",
                    "annotation": annotation.to_dict(),
                }
            ),
            201,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@annotations_bp.route("/<annotation_id>", methods=["GET"])
@jwt_required()
def get_annotation(annotation_id):
    """Get a specific annotation by ID."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401
        annotation = Annotation.query.get(annotation_id)
        if not annotation:
            return jsonify({"error": "Annotation not found"}), 404
        return jsonify({"annotation": annotation.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
