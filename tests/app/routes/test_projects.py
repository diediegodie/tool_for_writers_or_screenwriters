"""
Unit tests for GET/POST/PUT /projects endpoints.
"""

import pytest
from backend.app import create_app, db
from backend.app.services.auth_service import AuthService
from backend.models.user import User
from backend.models.project import Project
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


@pytest.fixture
def auth_header():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.app_context():
        # Import all models to register them for table creation
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
        user = User(
            id=str(uuid.uuid4()),
            email="projuser@example.com",
            password_hash=AuthService.hash_password("password123"),
        )
        db.session.add(user)
        db.session.commit()
        token = AuthService.generate_token(str(user.id))
        return {"Authorization": f"Bearer {token}"}, str(user.id)


def test_get_projects_empty(test_client, auth_header):
    """Normal case: user with no projects gets empty list."""
    headers, _ = auth_header
    resp = test_client.get("/projects/", headers=headers)
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_create_project_success(test_client, auth_header):
    """Normal case: create project returns project data."""
    headers, user_id = auth_header
    data = {"title": "My Book", "description": "A test project."}
    resp = test_client.post("/projects/", json=data, headers=headers)
    assert resp.status_code == 201
    result = resp.get_json()
    assert result["title"] == "My Book"
    assert result["description"] == "A test project."
    # Confirm project is created
    with test_client.application.app_context():
        project = db.session.query(Project).filter_by(user_id=user_id).first()
        assert project is not None
        assert project.title == "My Book"


def test_create_project_invalid_input(test_client, auth_header):
    """Edge case: missing title returns 400."""
    headers, _ = auth_header
    resp = test_client.post(
        "/projects/", json={"description": "No title"}, headers=headers
    )
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "Validation error"


def test_update_project_success(test_client, auth_header):
    """Normal case: update project returns updated data."""
    headers, user_id = auth_header
    # Create project first
    with test_client.application.app_context():
        project = Project(
            id=str(uuid.uuid4()),
            user_id=user_id,
            title="Old Title",
            description="Old desc",
        )
        db.session.add(project)
        db.session.commit()
        pid = str(project.id)
    data = {"title": "New Title", "description": "New desc"}
    resp = test_client.put(f"/projects/{pid}", json=data, headers=headers)
    assert resp.status_code == 200
    result = resp.get_json()
    assert result["title"] == "New Title"
    assert result["description"] == "New desc"


def test_update_project_not_found(test_client, auth_header):
    """Failure case: updating non-existent project returns 404."""
    headers, _ = auth_header
    pid = str(uuid.uuid4())
    resp = test_client.put(f"/projects/{pid}", json={"title": "Nope"}, headers=headers)
    assert resp.status_code == 404
    assert resp.get_json()["error"] == "Project not found"


def test_update_project_invalid_input(test_client, auth_header):
    """Edge case: invalid update data returns 400."""
    headers, user_id = auth_header
    # Create project first
    with test_client.application.app_context():
        project = Project(
            id=str(uuid.uuid4()), user_id=user_id, title="Title", description="Desc"
        )
        db.session.add(project)
        db.session.commit()
        pid = str(project.id)
    resp = test_client.put(f"/projects/{pid}", json={"title": ""}, headers=headers)
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "Validation error"
