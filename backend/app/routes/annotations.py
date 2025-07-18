"""
Annotation routes for GET/POST /annotations/
"""

from flask import Blueprint, request, jsonify
from backend.models.annotation import Annotation
from backend.app import db
from backend.app.schemas.annotation_schema import AnnotationSchema
from flask_jwt_extended import jwt_required

bp = Blueprint("annotations", __name__, url_prefix="/annotations")

annotation_schema = AnnotationSchema()
annotations_schema = AnnotationSchema(many=True)


@bp.route("/", methods=["GET"])
@jwt_required()
def get_annotations():
    """Get all annotations."""
    annotations = Annotation.query.all()
    return jsonify(annotations_schema.dump(annotations)), 200


@bp.route("/", methods=["POST"])
@jwt_required()
def create_annotation():
    """Create a new annotation."""
    data = request.get_json()
    errors = annotation_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    annotation = Annotation(
        draft_id=data["draft_id"],
        context=data.get("context", ""),
        highlight=data.get("highlight", ""),
    )
    db.session.add(annotation)
    db.session.commit()
    return jsonify(annotation_schema.dump(annotation)), 201
