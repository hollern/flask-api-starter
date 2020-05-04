from app.models.utils import CoreModel, CoreSchema
from marshmallow import fields
from app import db

from sqlalchemy.dialects.postgresql import UUID


class UnitSchema(CoreSchema):
    name = fields.String(required=True)
    linked_property = fields.UUID(required=True)


class Unit(CoreModel):
    __tablename__ = 'units'
    name = db.Column(db.String(99), nullable=False)
    linked_property = db.Column(UUID(as_uuid=True), db.ForeignKey('properties.id'), index=True, nullable=False)

    # Relationships
    work_requests = db.relationship('WorkRequest', backref='unit', lazy='dynamic')
    documents = db.relationship('Document', backref='unit', lazy='dynamic')
    leases = db.relationship('Lease', backref='unit', lazy='dynamic')
    notes = db.relationship('Note', backref='unit', lazy='dynamic')

    # Schemas
    single_schema = UnitSchema()
    many_schema = UnitSchema(many=True)
