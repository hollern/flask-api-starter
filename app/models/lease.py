from app.models.utils import CoreModel, CoreSchema
from app.models import tenants_on_leases
from marshmallow import fields
from app import db

from sqlalchemy.dialects.postgresql import UUID


class LeaseSchema(CoreSchema):
    rent_cycle = fields.String()
    first_due_date = fields.Date()
    amount_due = fields.Float()
    memo = fields.String()
    security_deposit_amount = fields.Float()
    is_security_deposit_paid = fields.Boolean()
    is_lease_signed = fields.Boolean()
    linked_unit = fields.UUID(required=True)


class Lease(CoreModel):
    __tablename__ = 'leases'
    rent_cycle = db.Column(db.String(19))
    first_due_date = db.Column(db.Date)
    amount_due = db.Column(db.Float)
    memo = db.Column(db.String(299))
    security_deposit_amount = db.Column(db.Float)
    is_security_deposit_paid = db.Column(db.Boolean, default=False)
    is_lease_signed = db.Column(db.Boolean, default=False)
    linked_unit = db.Column(UUID(as_uuid=True), db.ForeignKey('units.id'), index=True, nullable=False)

    # Relationships
    documents = db.relationship('Document', backref='lease', lazy='dynamic')
    payments_made = db.relationship('PaymentMade', backref='lease', lazy='dynamic')
    payments_due = db.relationship('PaymentDue', backref='lease', lazy='dynamic')
    notes = db.relationship('Note', backref='lease', lazy='dynamic')
    tenants = db.relationship('Tenant', secondary=tenants_on_leases,
                              backref=db.backref('lease', lazy='dynamic'), lazy='dynamic')

    # Schemas
    single_schema = LeaseSchema()
    many_schema = LeaseSchema(many=True)
