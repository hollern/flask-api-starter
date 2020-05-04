from app.models.utils import CoreModel, CoreSchema
from marshmallow import fields
from app import db

from sqlalchemy.dialects.postgresql import UUID


class WorkRequestSchema(CoreSchema):
    subject = fields.String(required=True)
    is_entry_allowed = fields.Boolean()
    status = fields.String()
    priority = fields.String()
    date_completed = fields.Date()
    date_opened = fields.Date()
    linked_tenant = fields.UUID(required=True)
    linked_unit = fields.UUID(required=True)


class WorkRequest(CoreModel):
    __tablename__ = 'work_requests'
    subject = db.Column(db.String(99))
    is_entry_allowed = db.Column(db.Boolean)
    status = db.Column(db.String(29))
    priority = db.Column(db.String(29))
    date_completed = db.Column(db.Date)
    date_opened = db.Column(db.Date)
    linked_tenant = db.Column(UUID(as_uuid=True), db.ForeignKey('tenants.id'), index=True, nullable=False)
    linked_unit = db.Column(UUID(as_uuid=True), db.ForeignKey('units.id'), index=True, nullable=False)

    # Relationships
    documents = db.relationship('Document', backref='work_request', lazy='dynamic')
    notes = db.relationship('Note', backref='work_request', lazy='dynamic')

    # Schemas
    single_schema = WorkRequestSchema()
    many_schema = WorkRequestSchema(many=True)
