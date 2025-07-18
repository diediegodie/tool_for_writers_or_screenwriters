import pytest


@pytest.fixture
def test_client():
    from backend.app import create_app, db

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


import uuid
import pytest
from backend.app import db
from backend.models.scene import Scene
from backend.models.chapter import Chapter
from backend.models.user import User
from backend.models.project import Project
from backend.app.services.auth_service import AuthService


@pytest.fixture
def auth_header_and_project():
    from backend.app import create_app

    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.app_context():
        db.create_all()
        user = User(
            id=str(uuid.uuid4()),
            email="sceneuser@example.com",
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


"""
Unit tests for GET/POST/PUT /scenes endpoints.
"""

import pytest
import uuid
from backend.app import db
from backend.models.scene import Scene
from backend.models.chapter import Chapter


@pytest.fixture
def chapter_for_scene(test_client, auth_header_and_project):
    headers, user_id, project_id = auth_header_and_project
    with test_client.application.app_context():
        chapter = Chapter(
            id=str(uuid.uuid4()), project_id=project_id, title="Test Chapter", order=1
        )
        db.session.add(chapter)
        db.session.commit()
        return chapter.id


@pytest.mark.usefixtures("auth_header_and_project")
def test_get_scenes_empty(test_client, auth_header_and_project, chapter_for_scene):
    headers, _, _ = auth_header_and_project
    chapter_id = chapter_for_scene
    resp = test_client.get(f"/scenes/?chapter_id={chapter_id}", headers=headers)
    assert resp.status_code == 200
    assert resp.json == []


@pytest.mark.usefixtures("auth_header_and_project")
def test_create_scene_success(test_client, auth_header_and_project, chapter_for_scene):
    headers, _, _ = auth_header_and_project
    chapter_id = chapter_for_scene
    data = {"chapter_id": chapter_id, "title": "Scene 1", "order": 1}
    resp = test_client.post("/scenes/", json=data, headers=headers)
    assert resp.status_code == 201
    assert resp.json["title"] == "Scene 1"
    assert resp.json["chapter_id"] == chapter_id


@pytest.mark.usefixtures("auth_header_and_project")
def test_create_scene_invalid_input(test_client, auth_header_and_project):
    headers, _, _ = auth_header_and_project
    data = {"title": "Scene 1"}  # Missing chapter_id and order
    resp = test_client.post("/scenes/", json=data, headers=headers)
    assert resp.status_code == 400
    assert "chapter_id" in resp.json
    assert "order" in resp.json


@pytest.mark.usefixtures("auth_header_and_project")
def test_update_scene_success(test_client, auth_header_and_project, chapter_for_scene):
    headers, _, _ = auth_header_and_project
    chapter_id = chapter_for_scene
    with test_client.application.app_context():
        scene = Scene(
            id=str(uuid.uuid4()), chapter_id=chapter_id, title="Old Title", order=1
        )
        db.session.add(scene)
        db.session.commit()
        scene_id = scene.id
    data = {"title": "New Title", "order": 2}
    resp = test_client.put(f"/scenes/{scene_id}", json=data, headers=headers)
    assert resp.status_code == 200
    assert resp.json["title"] == "New Title"
    assert resp.json["order"] == 2


@pytest.mark.usefixtures("auth_header_and_project")
def test_update_scene_not_found(test_client, auth_header_and_project):
    headers, _, _ = auth_header_and_project
    sid = str(uuid.uuid4())
    resp = test_client.put(f"/scenes/{sid}", json={"title": "Nope"}, headers=headers)
    assert resp.status_code == 404
    assert "error" in resp.json


@pytest.mark.usefixtures("auth_header_and_project")
def test_update_scene_invalid_input(
    test_client, auth_header_and_project, chapter_for_scene
):
    headers, _, _ = auth_header_and_project
    chapter_id = chapter_for_scene
    with test_client.application.app_context():
        scene = Scene(
            id=str(uuid.uuid4()), chapter_id=chapter_id, title="Title", order=1
        )
        db.session.add(scene)
        db.session.commit()
        scene_id = scene.id
    resp = test_client.put(
        f"/scenes/{scene_id}", json={"order": "not-an-int"}, headers=headers
    )
    assert resp.status_code == 400
    assert "order" in resp.json
