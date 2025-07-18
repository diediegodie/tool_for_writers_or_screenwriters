"""
Routes for GET/POST/PUT /scenes endpoints.
"""

from flask import Blueprint, request, jsonify
from backend.models.scene import Scene
from backend.app import db
from backend.app.schemas.scene_schema import SceneSchema
from backend.app.utils.jwt_required import jwt_required
import uuid

scenes_bp = Blueprint("scenes", __name__, url_prefix="/scenes")
bp = scenes_bp
scene_schema = SceneSchema()


@scenes_bp.route("/", methods=["GET"])
@jwt_required
def get_scenes():
    chapter_id = request.args.get("chapter_id")
    if not chapter_id:
        return jsonify({"error": "chapter_id required"}), 400
    scenes = (
        db.session.query(Scene)
        .filter_by(chapter_id=chapter_id)
        .order_by(Scene.order)
        .all()
    )
    return jsonify(scene_schema.dump(scenes, many=True)), 200


@scenes_bp.route("/", methods=["POST"])
@jwt_required
def create_scene():
    data = request.get_json()
    errors = scene_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    scene = Scene(
        id=str(uuid.uuid4()),
        chapter_id=data["chapter_id"],
        title=data["title"],
        content=data.get("content"),
        order=data["order"],
    )
    db.session.add(scene)
    db.session.commit()
    return jsonify(scene_schema.dump(scene)), 201


@scenes_bp.route("/<scene_id>", methods=["PUT"])
@jwt_required
def update_scene(scene_id):
    scene = db.session.query(Scene).filter_by(id=scene_id).first()
    if not scene:
        return jsonify({"error": "Scene not found"}), 404
    data = request.get_json()
    errors = scene_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400
    if "title" in data:
        scene.title = data["title"]
    if "content" in data:
        scene.content = data["content"]
    if "order" in data:
        scene.order = data["order"]
    db.session.commit()
    return jsonify(scene_schema.dump(scene)), 200
