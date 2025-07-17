"""
Authentication routes for user login, registration, and JWT management.
"""

from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user account.

    Expected JSON:
        {
            "email": "user@example.com",
            "username": "username",
            "password": "password",
            "first_name": "John",
            "last_name": "Doe"
        }
    """
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ["email", "username", "password", "first_name", "last_name"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"{field} is required"}), 400

        # Check if user already exists
        if User.find_by_email(data["email"]):
            return jsonify({"error": "Email already registered"}), 400

        if User.find_by_username(data["username"]):
            return jsonify({"error": "Username already taken"}), 400

        # Create new user
        user = User(
            email=data["email"].lower(),
            username=data["username"].lower(),
            first_name=data["first_name"],
            last_name=data["last_name"],
        )
        user.set_password(data["password"])
        user.save()

        # Generate JWT token
        access_token = create_access_token(identity=user.id)
        return (
            jsonify(
                {
                    "message": "User registered successfully",
                    "user": user.to_dict(),
                    "access_token": access_token,
                }
            ),
            201,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login user and return JWT token.

    Expected JSON:
        {
            "email": "user@example.com",
            "password": "password"
        }
    """
    try:
        data = request.get_json()

        # Validate required fields
        if not data.get("email") or not data.get("password"):
            return jsonify({"error": "Email and password are required"}), 400

        # Find user by email
        user = User.find_by_email(data["email"])
        if not user or not user.check_password(data["password"]):
            return jsonify({"error": "Invalid email or password"}), 401

        if not user.is_active:
            return jsonify({"error": "Account is deactivated"}), 401

        # Generate JWT token
        access_token = create_access_token(identity=user.id)
        return (
            jsonify(
                {
                    "message": "Login successful",
                    "user": user.to_dict(),
                    "access_token": access_token,
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    """Get current user information from JWT token."""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"user": user.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
