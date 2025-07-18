"""
Unit tests for models: User, Project, Chapter, Scene, Draft, Annotation, Export, AutosaveVersion
"""

import pytest
from backend.app import create_app, db
from backend.models.user import User
from backend.models.project import Project
from backend.models.chapter import Chapter
from backend.models.scene import Scene
from backend.models.draft import Draft
from backend.models.annotation import Annotation
from backend.models.export import Export
from backend.models.autosave_version import AutosaveVersion
from datetime import datetime


@pytest.fixture
def app():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


def test_user_model(app):
    with app.app_context():
        user = User(id="user-uuid", email="test@example.com", password_hash="hash")
        db.session.add(user)
        db.session.commit()
        assert User.query.count() == 1
        assert User.query.first().email == "test@example.com"


def test_project_model(app):
    with app.app_context():
        user = User(id="user-uuid", email="test@example.com", password_hash="hash")
        db.session.add(user)
        db.session.commit()
        project = Project(id="proj-uuid", user_id="user-uuid", title="Title")
        db.session.add(project)
        db.session.commit()
        assert Project.query.count() == 1
        assert Project.query.first().title == "Title"


def test_chapter_model(app):
    with app.app_context():
        project = Project(id="proj-uuid", user_id="user-uuid", title="Title")
        db.session.add(project)
        db.session.commit()
        chapter = Chapter(id="chap-uuid", project_id="proj-uuid", title="Chap", order=1)
        db.session.add(chapter)
        db.session.commit()
        assert Chapter.query.count() == 1
        assert Chapter.query.first().title == "Chap"


def test_scene_model(app):
    with app.app_context():
        project = Project(id="proj-uuid", user_id="user-uuid", title="Title")
        db.session.add(project)
        db.session.commit()
        chapter = Chapter(id="chap-uuid", project_id="proj-uuid", title="Chap", order=1)
        db.session.add(chapter)
        db.session.commit()
        scene = Scene(id="scene-uuid", chapter_id="chap-uuid", title="Scene", order=1)
        db.session.add(scene)
        db.session.commit()
        assert Scene.query.count() == 1
        assert Scene.query.first().title == "Scene"


def test_draft_model(app):
    with app.app_context():
        draft = Draft(id="draft-uuid", scene_id="scene-uuid", content="Draft")
        db.session.add(draft)
        db.session.commit()
        assert Draft.query.count() == 1
        assert Draft.query.first().content == "Draft"


def test_annotation_model(app):
    with app.app_context():
        annotation = Annotation(
            id="ann-uuid", draft_id="draft-uuid", context="Ctx", highlight="HL"
        )
        db.session.add(annotation)
        db.session.commit()
        assert Annotation.query.count() == 1
        assert Annotation.query.first().highlight == "HL"


def test_export_model(app):
    with app.app_context():
        export = Export(
            id="exp-uuid",
            user_id="user-uuid",
            project_id="proj-uuid",
            export_type="docx",
            file_path="file.docx",
            created_at=datetime.utcnow(),
        )
        db.session.add(export)
        db.session.commit()
        assert Export.query.count() == 1
        assert Export.query.first().export_type == "docx"


def test_autosave_version_model(app):
    with app.app_context():
        autosave = AutosaveVersion(
            id="auto-uuid",
            scene_id="scene-uuid",
            content="Auto",
            saved_at=datetime.utcnow(),
        )
        db.session.add(autosave)
        db.session.commit()
        assert AutosaveVersion.query.count() == 1
        assert AutosaveVersion.query.first().content == "Auto"
