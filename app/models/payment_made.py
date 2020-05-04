from app.models.utils import CoreModel, CoreSchema
from marshmallow import fields
from app import db

from sqlalchemy.dialects.postgresql import UUID


class PaymentMadeSchema(CoreSchema):
    paid_date = fields.Date(required=True)
    amount = fields.Float(required=True)
    linked_tenant = fields.UUID(required=True)
    linked_lease = fields.UUID(required=True)


class PaymentMade(CoreModel):
    __tablename__ = 'payments_made'
    paid_date = db.Column(db.Date)
    amount = db.Column(db.Float)
    linked_tenant = db.Column(UUID(as_uuid=True), db.ForeignKey('tenants.id'), nullable=False)
    linked_lease = db.Column(UUID(as_uuid=True), db.ForeignKey('leases.id'), nullable=False)

    # Schemas
    single_schema = PaymentMadeSchema()
    many_schema = PaymentMadeSchema(many=True)
