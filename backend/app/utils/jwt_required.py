"""
JWT-required decorator for protecting Flask routes.
"""

from functools import wraps
from flask import request, jsonify
from backend.app.services.auth_service import AuthService


def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        payload = AuthService.decode_token(token)
        if not payload:
            return jsonify({"error": "Token is invalid or expired"}), 401
        request.user_id = payload["user_id"]
        return f(*args, **kwargs)

    return decorated_function
