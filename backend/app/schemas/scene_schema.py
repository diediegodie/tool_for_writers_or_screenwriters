"""
Marshmallow schema for Scene endpoints.
"""

from marshmallow import Schema, fields


class SceneSchema(Schema):
    id = fields.String(dump_only=True)
    chapter_id = fields.String(required=True)
    title = fields.String(required=True)
    content = fields.String(allow_none=True)
    order = fields.Integer(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
