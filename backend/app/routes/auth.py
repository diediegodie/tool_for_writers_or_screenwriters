"""
Auth routes for user registration and login.
"""

from flask import Blueprint, request, jsonify, current_app
from backend.models.user import User
from backend.app import db
from backend.app.services.auth_service import AuthService
import uuid

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["POST"])
def register():
    """
    POST /auth/register
    Register a new user and return JWT token.

    Request JSON:
        {
            "email": "user@example.com",
            "password": "password123"
        }
    Response:
        201: {"token": "<jwt>"}
        400: {"error": "Validation error"}
        409: {"error": "Email already registered"}
    """
    from backend.app.schemas.register_schema import RegisterSchema

    schema = RegisterSchema()
    data = request.get_json()
    errors = schema.validate(data)
    if errors:
        # Reason: Input validation failed
        return jsonify({"error": "Validation error", "details": errors}), 400
    email = data["email"]
    password = data["password"]
    if db.session.query(User).filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409
    user = User(
        id=str(uuid.uuid4()),
        email=email,
        password_hash=AuthService.hash_password(password),
    )
    db.session.add(user)
    db.session.commit()
    token = AuthService.generate_token(str(user.id))
    return jsonify({"token": token}), 201


@bp.route("/login", methods=["POST"])
def login():
    """
    POST /auth/login
    Authenticate user and return JWT token.

    Request JSON:
        {
            "email": "user@example.com",
            "password": "password123"
        }
    Response:
        200: {"token": "<jwt>"}
        400: {"error": "Validation error"}
        401: {"error": "Invalid credentials"}
    """
    from backend.app.schemas.auth_schema import LoginSchema

    schema = LoginSchema()
    data = request.get_json()
    errors = schema.validate(data)
    if errors:
        # Reason: Input validation failed
        return jsonify({"error": "Validation error", "details": errors}), 400
    email = data["email"]
    password = data["password"]
    user = db.session.query(User).filter_by(email=email).first()
    if not user or not AuthService.verify_password(password, user.password_hash):
        # Reason: Invalid credentials
        return jsonify({"error": "Invalid credentials"}), 401
    token = AuthService.generate_token(str(user.id))
    return jsonify({"token": token}), 200
