"""
Unit tests for GET /timeline/<project_id> endpoint.
"""

import pytest
from backend.app import create_app, db
from backend.models.project import Project
from backend.models.chapter import Chapter
from backend.models.scene import Scene
from flask_jwt_extended import create_access_token, JWTManager
from datetime import datetime


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


def test_get_timeline_normal(client, auth_header):
    """Normal case: timeline with chapters and scenes."""
    with client.application.app_context():
        project = Project(id="proj-uuid", user_id="user-uuid", title="My Project")
        db.session.add(project)
        chapter = Chapter(
            id="chap-uuid",
            project_id="proj-uuid",
            title="Chapter 1",
            order=1,
            created_at=datetime.utcnow(),
        )
        db.session.add(chapter)
        scene = Scene(
            id="scene-uuid",
            chapter_id="chap-uuid",
            title="Scene 1",
            order=1,
            created_at=datetime.utcnow(),
        )
        db.session.add(scene)
        db.session.commit()
    rv = client.get("/timeline/proj-uuid", headers=auth_header)
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["project_id"] == "proj-uuid"
    assert data["timeline"][0]["chapter_id"] == "chap-uuid"
    assert data["timeline"][0]["scenes"][0]["scene_id"] == "scene-uuid"


def test_get_timeline_no_project(client, auth_header):
    """Failure case: project not found."""
    rv = client.get("/timeline/doesnotexist", headers=auth_header)
    assert rv.status_code == 404
    assert "error" in rv.get_json()


def test_get_timeline_empty(client, auth_header):
    """Edge case: project with no chapters/scenes."""
    with client.application.app_context():
        project = Project(id="proj-empty", user_id="user-uuid", title="Empty Project")
        db.session.add(project)
        db.session.commit()
    rv = client.get("/timeline/proj-empty", headers=auth_header)
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["project_id"] == "proj-empty"
    assert data["timeline"] == []
