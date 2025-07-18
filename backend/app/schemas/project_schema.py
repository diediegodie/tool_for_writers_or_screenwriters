from marshmallow import Schema, fields, validate


class ProjectCreateSchema(Schema):
    """Schema for creating a new project."""

    title = fields.String(required=True, validate=validate.Length(min=1, max=200))
    description = fields.String(validate=validate.Length(max=500))


class ProjectUpdateSchema(Schema):
    """Schema for updating an existing project."""

    title = fields.String(validate=validate.Length(min=1, max=200))
    description = fields.String(validate=validate.Length(max=500))
