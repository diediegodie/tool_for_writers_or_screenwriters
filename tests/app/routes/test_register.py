"""
Unit tests for POST /auth/register endpoint.
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


def test_register_success(test_client):
    """Normal case: valid registration returns token."""
    email = "newuser@example.com"
    password = "password123"
    resp = test_client.post(
        "/auth/register", json={"email": email, "password": password}
    )
    assert resp.status_code == 201
    assert "token" in resp.get_json()
    # Confirm user is created
    with test_client.application.app_context():
        user = db.session.query(User).filter_by(email=email).first()
        assert user is not None
        assert AuthService.verify_password(password, user.password_hash)


def test_register_duplicate_email(test_client):
    """Failure case: duplicate email returns 409."""
    email = "dupe@example.com"
    password = "password123"
    # Create user first
    with test_client.application.app_context():
        user = User(
            id=str(uuid.uuid4()),
            email=email,
            password_hash=AuthService.hash_password(password),
        )
        db.session.add(user)
        db.session.commit()
    resp = test_client.post(
        "/auth/register", json={"email": email, "password": password}
    )
    assert resp.status_code == 409
    assert resp.get_json()["error"] == "Email already registered"


def test_register_invalid_input(test_client):
    """Edge case: missing or invalid fields returns 400."""
    resp = test_client.post(
        "/auth/register", json={"email": "not-an-email", "password": "123"}
    )
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "Validation error"
    resp2 = test_client.post("/auth/register", json={"email": "", "password": ""})
    assert resp2.status_code == 400
    assert resp2.get_json()["error"] == "Validation error"
