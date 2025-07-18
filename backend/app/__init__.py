"""
App factory for backend Flask app.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from backend.config import Config  # Reason: Use absolute import for installable package

# Reason: Single DB instance for all models
db = SQLAlchemy()
migrate = Migrate()


# Reason: App factory pattern for scalability
def create_app(config_override=None):
    """
    App factory for backend Flask app.
    Accepts optional config_override dict for testing or custom configs.
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    if config_override:
        app.config.update(config_override)
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    # Reason: Import models to register with SQLAlchemy
    # Reason: Import models to register with SQLAlchemy
    import backend.models  # Reason: Only import for registration, not direct usage

    # Register blueprints
    from backend.app.routes.auth import bp as auth_bp
    from backend.app.routes.projects import bp as projects_bp
    from backend.app.routes.chapters import bp as chapters_bp
    from backend.app.routes.scenes import bp as scenes_bp
    from backend.app.routes.drafts import bp as drafts_bp
    from backend.app.routes.annotations import bp as annotations_bp
    from backend.app.routes.timeline import bp as timeline_bp
    from backend.app.routes.autosave import bp as autosave_bp
    from backend.app.routes.export import bp as export_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(chapters_bp)
    app.register_blueprint(scenes_bp)
    app.register_blueprint(drafts_bp)
    app.register_blueprint(annotations_bp)
    app.register_blueprint(timeline_bp)
    app.register_blueprint(autosave_bp)
    app.register_blueprint(export_bp)
    return app
