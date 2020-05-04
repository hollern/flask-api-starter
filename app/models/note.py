from app.models.utils import CoreModel, CoreSchema
from marshmallow import fields
from app import db

from sqlalchemy.dialects.postgresql import UUID


class NoteSchema(CoreSchema):
    text = fields.String(required=True)
    linked_user = fields.UUID(required=True)
    linked_lease = fields.UUID()
    linked_property = fields.UUID()
    linked_unit = fields.UUID()
    linked_work_request = fields.UUID()


class Note(CoreModel):
    __tablename__ = 'notes'
    text = db.Column(db.String(499))
    linked_user = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), index=True, nullable=False)

    # Optional foreign keys
    linked_lease = db.Column(UUID(as_uuid=True), db.ForeignKey('leases.id'), index=True)
    linked_property = db.Column(UUID(as_uuid=True), db.ForeignKey('properties.id'), index=True)
    linked_unit = db.Column(UUID(as_uuid=True), db.ForeignKey('units.id'), index=True)
    linked_work_request = db.Column(UUID(as_uuid=True), db.ForeignKey('work_requests.id'), index=True)

    # Schemas
    single_schema = NoteSchema()
    many_schema = NoteSchema(many=True)
