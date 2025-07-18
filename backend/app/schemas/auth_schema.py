from marshmallow import Schema, fields, validate


class LoginSchema(Schema):
    """Schema for user login request validation."""

    email = fields.Email(required=True, validate=validate.Length(max=255))
    password = fields.String(required=True, validate=validate.Length(min=6, max=128))
