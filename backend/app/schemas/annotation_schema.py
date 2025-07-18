"""
Annotation schema for validation and serialization.
"""

from marshmallow import Schema, fields


class AnnotationSchema(Schema):
    id = fields.Str(dump_only=True)
    draft_id = fields.Str(required=True)
    context = fields.Str()
    highlight = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
