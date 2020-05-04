from app.models.utils import CoreModel, CoreSchema
from app.models import communications_with_tenants
from marshmallow import fields, validate
from datetime import datetime
from app import db


class CommunicationSchema(CoreSchema):
    text = fields.String(required=True)
    sent_time = fields.DateTime()
    communication_type = fields.String(required=True, validate=validate.OneOf(['email', 'sms', 'announcement']))


class Communication(CoreModel):
    __tablename__ = 'communications'
    text = db.Column(db.String(499))
    sent_time = db.Column(db.DateTime, default=datetime.utcnow)
    communication_type = db.Column(db.String(29))

    # Relationships
    tenants = db.relationship('Tenant', secondary=communications_with_tenants,
                              backref=db.backref('communication', lazy='dynamic'), lazy='dynamic')

    # Schemas
    single_schema = CommunicationSchema()
    many_schema = CommunicationSchema(many=True)
