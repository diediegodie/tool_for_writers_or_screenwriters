from marshmallow import Schema, fields, validate


class ChapterCreateSchema(Schema):
    """Schema for creating a new chapter."""

    project_id = fields.String(required=True, validate=validate.Length(equal=36))
    title = fields.String(required=True, validate=validate.Length(min=1, max=200))
    order = fields.Integer(required=True)


class ChapterUpdateSchema(Schema):
    """Schema for updating an existing chapter."""

    title = fields.String(validate=validate.Length(min=1, max=200))
    order = fields.Integer()
