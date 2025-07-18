"""
Authentication service for JWT-based user authentication.
"""

from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from flask import current_app


class AuthService:
    """
    Service for handling password hashing and JWT token generation/validation.
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password for storing."""
        return generate_password_hash(password)

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verify a stored password against one provided by user."""
        return check_password_hash(password_hash, password)

    @staticmethod
    def generate_token(user_id: str, expires_in: int = 3600) -> str:
        """Generate JWT token for a user."""
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(seconds=expires_in),
        }
        secret = current_app.config["SECRET_KEY"]
        return jwt.encode(payload, secret, algorithm="HS256")

    @staticmethod
    def decode_token(token: str):
        """Decode JWT token and return payload or None if invalid."""
        secret = current_app.config["SECRET_KEY"]
        try:
            payload = jwt.decode(token, secret, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
