"""
Unit tests for POST /autosave endpoint.
"""

import pytest
from backend.app import create_app, db
from backend.models.autosave_version import AutosaveVersion
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


def test_post_autosave_scene(client, auth_header):
    """Normal case: autosave for scene."""
    data = {"scene_id": "scene-uuid", "content": "Scene autosave."}
    rv = client.post("/autosave/", json=data, headers=auth_header)
    assert rv.status_code == 201
    assert rv.get_json()["scene_id"] == "scene-uuid"
    assert rv.get_json()["content"] == "Scene autosave."


def test_post_autosave_draft(client, auth_header):
    """Normal case: autosave for draft."""
    data = {"draft_id": "draft-uuid", "content": "Draft autosave."}
    rv = client.post("/autosave/", json=data, headers=auth_header)
    assert rv.status_code == 201
    assert rv.get_json()["draft_id"] == "draft-uuid"
    assert rv.get_json()["content"] == "Draft autosave."


def test_post_autosave_missing_content(client, auth_header):
    """Failure case: missing content."""
    data = {"scene_id": "scene-uuid"}
    rv = client.post("/autosave/", json=data, headers=auth_header)
    assert rv.status_code == 400
    assert "content" in rv.get_json()


def test_post_autosave_missing_ids(client, auth_header):
    """Edge case: missing scene_id and draft_id."""
    data = {"content": "No ids."}
    rv = client.post("/autosave/", json=data, headers=auth_header)
    assert rv.status_code == 400
    assert "error" in rv.get_json()
