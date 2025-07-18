"""
Unit tests for GET/POST /annotations/ endpoint.
"""

import pytest
from backend.app import create_app, db
from backend.models.annotation import Annotation
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


def test_get_annotations_empty(client, auth_header):
    """Normal case: GET returns empty list."""
    rv = client.get("/annotations/", headers=auth_header)
    assert rv.status_code == 200
    assert rv.get_json() == []


def test_post_annotation_normal(client, auth_header):
    """Normal case: POST creates an annotation."""
    data = {
        "draft_id": "draft-uuid",
        "context": "Some context",
        "highlight": "Some highlight",
    }
    rv = client.post("/annotations/", json=data, headers=auth_header)
    assert rv.status_code == 201
    assert rv.get_json()["draft_id"] == "draft-uuid"
    assert rv.get_json()["context"] == "Some context"
    assert rv.get_json()["highlight"] == "Some highlight"


def test_post_annotation_missing_draft_id(client, auth_header):
    """Failure case: POST missing draft_id."""
    data = {"context": "No draft id", "highlight": "Highlight"}
    rv = client.post("/annotations/", json=data, headers=auth_header)
    assert rv.status_code == 400
    assert "draft_id" in rv.get_json()


def test_post_annotation_empty_highlight(client, auth_header):
    """Edge case: POST with empty highlight."""
    data = {"draft_id": "draft-uuid", "context": "Context", "highlight": ""}
    rv = client.post("/annotations/", json=data, headers=auth_header)
    assert rv.status_code == 201
    assert rv.get_json()["highlight"] == ""
