"""
User model for authentication and user management.
"""

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import BaseModel


class User(BaseModel, UserMixin):
    """
    User model for writers and screenwriters.
    Handles authentication and basic user information.
    """

    __tablename__ = "users"

    # User authentication fields
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # User profile fields
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.Text)

    # Account status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    email_verified = db.Column(db.Boolean, default=False, nullable=False)

    # Relationships
    projects = db.relationship(
        "Project", backref="author", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        """
        Hash and set user password.

        Args:
            password (str): Plain text password
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Check if provided password matches user's password.

        Args:
            password (str): Plain text password to check

        Returns:
            bool: True if password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """
        Convert user instance to dictionary (excluding sensitive data).

        Returns:
            dict: User data as dictionary
        """
        data = super().to_dict()
        data.update(
            {
                "email": self.email,
                "username": self.username,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "bio": self.bio,
                "is_active": self.is_active,
                "email_verified": self.email_verified,
            }
        )
        return data

    @staticmethod
    def find_by_email(email):
        """
        Find user by email address.

        Args:
            email (str): Email address to search for

        Returns:
            User: User instance or None
        """
        return User.query.filter_by(email=email.lower()).first()

    @staticmethod
    def find_by_username(username):
        """
        Find user by username.

        Args:
            username (str): Username to search for

        Returns:
            User: User instance or None
        """
        return User.query.filter_by(username=username.lower()).first()
