"""
AutosaveVersion schema for validation and serialization.
"""

from marshmallow import Schema, fields


class AutosaveVersionSchema(Schema):
    id = fields.Str(dump_only=True)
    scene_id = fields.Str()
    draft_id = fields.Str()
    content = fields.Str(required=True)
    saved_at = fields.DateTime(dump_only=True)
