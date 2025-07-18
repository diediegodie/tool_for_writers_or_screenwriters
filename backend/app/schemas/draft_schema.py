"""
Draft schema for validation and serialization.
"""

from marshmallow import Schema, fields


class DraftSchema(Schema):
    id = fields.Str(dump_only=True)
    scene_id = fields.Str(required=True)
    content = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
