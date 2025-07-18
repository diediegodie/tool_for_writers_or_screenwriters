"""
Unit tests for POST /auth/login endpoint.
"""

import pytest
from backend.app import create_app, db
from backend.app.services.auth_service import AuthService
from backend.models.user import User
import uuid


@pytest.fixture
def test_client():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.app_context():
        # Import all models to register them with SQLAlchemy for table creation
        from backend.models import (
            User,
            Project,
            Chapter,
            Scene,
            Draft,
            Annotation,
            AutosaveVersion,
            Export,
        )

        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


@pytest.fixture
def create_user():
    def _create(email, password):
        user = User(
            id=str(uuid.uuid4()),
            email=email,
            password_hash=AuthService.hash_password(password),
        )
        db.session.add(user)
        db.session.commit()
        return user

    return _create


def test_login_success(test_client, create_user):
    """Normal case: valid credentials return token."""
    email = "user@example.com"
    password = "password123"
    create_user(email, password)
    resp = test_client.post("/auth/login", json={"email": email, "password": password})
    assert resp.status_code == 200
    assert "token" in resp.get_json()


def test_login_invalid_password(test_client, create_user):
    """Failure case: wrong password returns 401."""
    email = "user@example.com"
    password = "password123"
    create_user(email, password)
    resp = test_client.post(
        "/auth/login", json={"email": email, "password": "wrongpass"}
    )
    assert resp.status_code == 401
    assert resp.get_json()["error"] == "Invalid credentials"


def test_login_missing_fields(test_client):
    """Edge case: missing fields returns 400."""
    resp = test_client.post("/auth/login", json={"email": ""})
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "Validation error"
