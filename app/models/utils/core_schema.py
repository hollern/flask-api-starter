from marshmallow import Schema, fields, RAISE


class CoreSchema(Schema):
    # id = fields.Integer(dump_only=True)
    # public_id = fields.String(dump_only=True)
    id = fields.UUID(dump_only=True)
    created = fields.DateTime(dump_only=True)
    modified = fields.DateTime(dump_only=True)

    class Meta:
        unknown = RAISE
