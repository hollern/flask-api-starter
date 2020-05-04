from app.models.utils import CoreModel, CoreSchema
from marshmallow import fields
from app import db

from sqlalchemy.dialects.postgresql import UUID


class PaymentDueSchema(CoreSchema):
    due_date = fields.Date(required=True)
    amount = fields.Float(required=True)
    linked_lease = fields.UUID(required=True)


class PaymentDue(CoreModel):
    __tablename__ = 'payments_due'
    due_date = db.Column(db.Date)
    amount = db.Column(db.Float)
    linked_lease = db.Column(UUID(as_uuid=True), db.ForeignKey('leases.id'), nullable=False)

    # Schemas
    single_schema = PaymentDueSchema()
    many_schema = PaymentDueSchema(many=True)
