"""
Export schema for validation and serialization.
"""

from marshmallow import Schema, fields


class ExportSchema(Schema):
    id = fields.Str(dump_only=True)
    user_id = fields.Str(required=True)
    project_id = fields.Str(required=True)
    export_type = fields.Str(required=True)
    file_path = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
