"""
Unit tests for GET/POST/PUT /chapters endpoints.
"""

import pytest
from backend.app import create_app, db
from backend.app.services.auth_service import AuthService
from backend.models.user import User
from backend.models.project import Project
from backend.models.chapter import Chapter
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
def auth_header_and_project():
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
        user = User(
            id=str(uuid.uuid4()),
            email="chapteruser@example.com",
            password_hash=AuthService.hash_password("password123"),
        )
        db.session.add(user)
        db.session.commit()
        project = Project(
            id=str(uuid.uuid4()),
            user_id=user.id,
            title="Test Project",
            description="Desc",
        )
        db.session.add(project)
        db.session.commit()
        token = AuthService.generate_token(str(user.id))
        return {"Authorization": f"Bearer {token}"}, str(user.id), str(project.id)


def test_get_chapters_empty(test_client, auth_header_and_project):
    """Normal case: project with no chapters returns empty list."""
    headers, _, project_id = auth_header_and_project
    resp = test_client.get(f"/chapters/?project_id={project_id}", headers=headers)
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_create_chapter_success(test_client, auth_header_and_project):
    """Normal case: create chapter returns chapter data."""
    headers, _, project_id = auth_header_and_project
    data = {"project_id": project_id, "title": "Chapter 1", "order": 1}
    resp = test_client.post("/chapters/", json=data, headers=headers)
    assert resp.status_code == 201
    result = resp.get_json()
    assert result["title"] == "Chapter 1"
    assert result["order"] == 1
    # Confirm chapter is created
    with test_client.application.app_context():
        chapter = db.session.query(Chapter).filter_by(project_id=project_id).first()
        assert chapter is not None
        assert chapter.title == "Chapter 1"


def test_create_chapter_invalid_input(test_client, auth_header_and_project):
    """Edge case: missing title returns 400."""
    headers, _, project_id = auth_header_and_project
    resp = test_client.post(
        "/chapters/", json={"project_id": project_id, "order": 1}, headers=headers
    )
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "Validation error"


def test_update_chapter_success(test_client, auth_header_and_project):
    """Normal case: update chapter returns updated data."""
    headers, _, project_id = auth_header_and_project
    # Create chapter first
    with test_client.application.app_context():
        chapter = Chapter(
            id=str(uuid.uuid4()), project_id=project_id, title="Old Title", order=1
        )
        db.session.add(chapter)
        db.session.commit()
        cid = str(chapter.id)
    data = {"title": "New Title", "order": 2}
    resp = test_client.put(f"/chapters/{cid}", json=data, headers=headers)
    assert resp.status_code == 200
    result = resp.get_json()
    assert result["title"] == "New Title"
    assert result["order"] == 2


def test_update_chapter_not_found(test_client, auth_header_and_project):
    """Failure case: updating non-existent chapter returns 404."""
    headers, _, _ = auth_header_and_project
    cid = str(uuid.uuid4())
    resp = test_client.put(f"/chapters/{cid}", json={"title": "Nope"}, headers=headers)
    assert resp.status_code == 404
    assert resp.get_json()["error"] == "Chapter not found"


def test_update_chapter_invalid_input(test_client, auth_header_and_project):
    """Edge case: invalid update data returns 400."""
    headers, _, project_id = auth_header_and_project
    # Create chapter first
    with test_client.application.app_context():
        chapter = Chapter(
            id=str(uuid.uuid4()), project_id=project_id, title="Title", order=1
        )
        db.session.add(chapter)
        db.session.commit()
        cid = str(chapter.id)
    resp = test_client.put(f"/chapters/{cid}", json={"title": ""}, headers=headers)
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "Validation error"
