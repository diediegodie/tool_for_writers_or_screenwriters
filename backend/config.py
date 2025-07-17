"""
Configuration settings for the Writer Tool application.
Handles different environments (development, testing, production).
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration with common settings."""

    # Secret key for JWT and session management
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"

    # Database configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    # JWT configuration
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

    # CORS configuration
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "http://localhost:3000").split(",")

    # File upload configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

    # Autosave configuration
    AUTOSAVE_INTERVAL_SECONDS = int(os.environ.get("AUTOSAVE_INTERVAL_SECONDS", "30"))
    AUTOSAVE_MAX_VERSIONS = int(os.environ.get("AUTOSAVE_MAX_VERSIONS", "50"))


class DevelopmentConfig(Config):
    """Development environment configuration."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DEV_DATABASE_URL")
        or "postgresql://postgres:password@localhost:5432/writer_tool_dev"
    )


class TestingConfig(Config):
    """Testing environment configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("TEST_DATABASE_URL")
        or "postgresql://postgres:password@localhost:5432/writer_tool_test"
    )
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production environment configuration."""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "postgresql://postgres:password@localhost:5432/writer_tool_prod"
    )

    # Enhanced security in production
    PERMANENT_SESSION_LIFETIME = timedelta(hours=12)


# Configuration mapping
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
