"""
Backend configuration for Flask app.
"""

import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "postgresql://writer_user:writer_pass@db:5432/writer_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_HEADERS = "Content-Type"
    DOCS_EXPORT_PATH = os.environ.get("DOCS_EXPORT_PATH", "/app/exports")
