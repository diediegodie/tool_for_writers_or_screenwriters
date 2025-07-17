"""
Flask application factory and initialization.
Creates and configures the Flask app with all extensions.
"""

from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name="default"):
    """
    Create and configure the Flask application.

    Args:
        config_name (str): Configuration environment name

    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)

    # Configure CORS
    CORS(app, origins=app.config["CORS_ORIGINS"])

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.projects import projects_bp
    from app.routes.chapters import chapters_bp
    from app.routes.scenes import scenes_bp

    from app.routes.exports import exports_bp
    from app.routes.autosave import autosave_bp
    from app.routes.drafts import drafts_bp
    from app.routes.annotations import annotations_bp
    from app.routes.timeline import timeline_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(projects_bp, url_prefix="/api/projects")
    app.register_blueprint(chapters_bp, url_prefix="/api/chapters")
    app.register_blueprint(scenes_bp, url_prefix="/api/scenes")
    app.register_blueprint(exports_bp, url_prefix="/api/exports")
    app.register_blueprint(autosave_bp, url_prefix="/api/autosave")
    app.register_blueprint(drafts_bp, url_prefix="/api/drafts")
    app.register_blueprint(annotations_bp, url_prefix="/api/annotations")
    app.register_blueprint(timeline_bp, url_prefix="/api/timeline")

    # Health check endpoint
    @app.route("/api/health")
    def health_check():
        """Simple health check endpoint."""
        return {"status": "healthy", "message": "Writer Tool API is running"}

    return app
