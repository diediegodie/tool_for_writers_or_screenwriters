"""
Unit tests for POST /export/<project_id> endpoint.
"""

import pytest
from backend.app import create_app, db
from backend.models.export import Export
from backend.models.project import Project
from backend.models.user import User
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
        user = User(id="user-uuid", email="testuser@example.com", password_hash="hash")
        db.session.add(user)
        db.session.commit()
        token = create_access_token(identity="user-uuid")
    return {"Authorization": f"Bearer {token}"}


def test_post_export_docx(client, auth_header):
    """Normal case: export project to docx."""
    with client.application.app_context():
        project = Project(id="proj-uuid", user_id="user-uuid", title="My Project")
        db.session.add(project)
        db.session.commit()
    data = {"export_type": "docx"}
    rv = client.post("/export/proj-uuid", json=data, headers=auth_header)
    assert rv.status_code == 200
    # Reason: Check export metadata in DB
    with client.application.app_context():
        export = Export.query.filter_by(
            project_id="proj-uuid", export_type="docx"
        ).first()
        assert export is not None
        assert export.user_id == "user-uuid"


def test_post_export_pdf(client, auth_header):
    """Normal case: export project to pdf."""
    with client.application.app_context():
        project = Project(id="proj-uuid2", user_id="user-uuid", title="My Project 2")
        db.session.add(project)
        db.session.commit()
    data = {"export_type": "pdf"}
    rv = client.post("/export/proj-uuid2", json=data, headers=auth_header)
    assert rv.status_code == 200
    # Reason: Check export metadata in DB
    with client.application.app_context():
        export = Export.query.filter_by(
            project_id="proj-uuid2", export_type="pdf"
        ).first()
        assert export is not None
        assert export.user_id == "user-uuid"


def test_post_export_invalid_type(client, auth_header):
    """Failure case: invalid export_type."""
    with client.application.app_context():
        project = Project(id="proj-uuid3", user_id="user-uuid", title="My Project 3")
        db.session.add(project)
        db.session.commit()
    data = {"export_type": "txt"}
    rv = client.post("/export/proj-uuid3", json=data, headers=auth_header)
    assert rv.status_code == 400
    assert "error" in rv.get_json()


def test_post_export_no_project(client, auth_header):
    """Edge case: project not found."""
    data = {"export_type": "docx"}
    rv = client.post("/export/doesnotexist", json=data, headers=auth_header)
    assert rv.status_code == 404
    assert "error" in rv.get_json()
