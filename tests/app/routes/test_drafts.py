"""
Unit tests for GET/POST /drafts/ endpoint.
"""

import pytest
from backend.app import create_app, db
from backend.models.draft import Draft
from flask_jwt_extended import create_access_token, JWTManager


@pytest.fixture
def client():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    JWTManager(app)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


@pytest.fixture
def auth_header(client):
    app = client.application
    with app.app_context():
        token = create_access_token(identity="testuser")
    return {"Authorization": f"Bearer {token}"}


def test_get_drafts_empty(client, auth_header):
    """Normal case: GET returns empty list."""
    rv = client.get("/drafts/", headers=auth_header)
    assert rv.status_code == 200
    assert rv.get_json() == []


def test_post_draft_normal(client, auth_header):
    """Normal case: POST creates a draft."""
    data = {"scene_id": "scene-uuid", "content": "Draft content."}
    rv = client.post("/drafts/", json=data, headers=auth_header)
    assert rv.status_code == 201
    assert rv.get_json()["scene_id"] == "scene-uuid"
    assert rv.get_json()["content"] == "Draft content."


def test_post_draft_missing_scene_id(client, auth_header):
    """Failure case: POST missing scene_id."""
    data = {"content": "No scene id."}
    rv = client.post("/drafts/", json=data, headers=auth_header)
    assert rv.status_code == 400
    assert "scene_id" in rv.get_json()


def test_post_draft_empty_content(client, auth_header):
    """Edge case: POST with empty content."""
    data = {"scene_id": "scene-uuid", "content": ""}
    rv = client.post("/drafts/", json=data, headers=auth_header)
    assert rv.status_code == 201
    assert rv.get_json()["content"] == ""
