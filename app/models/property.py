from app.models.utils import CoreModel, CoreSchema
from marshmallow import fields
from app import db

from sqlalchemy.dialects.postgresql import UUID


class PropertySchema(CoreSchema):
    name = fields.String(required=True)
    street_addr_line_1 = fields.String()
    street_addr_line_2 = fields.String()
    street_addr_line_3 = fields.String()
    city = fields.String()
    state = fields.String()
    zip = fields.String()
    country = fields.String()
    property_type = fields.String()
    linked_company = fields.UUID(required=True)


class Property(CoreModel):
    __tablename__ = 'properties'
    name = db.Column(db.String(99), nullable=False)
    street_addr_line_1 = db.Column(db.String(149))
    street_addr_line_2 = db.Column(db.String(149))
    street_addr_line_3 = db.Column(db.String(149))
    city = db.Column(db.String(149))
    state = db.Column(db.String(9))
    zip = db.Column(db.String(9))
    country = db.Column(db.String(99))
    property_type = db.Column(db.String(29))
    linked_company = db.Column(UUID(as_uuid=True), db.ForeignKey('companies.id'), index=True, nullable=False)

    # Relationships
    documents = db.relationship('Document', backref='property', lazy='dynamic')
    notes = db.relationship('Note', backref='property', lazy='dynamic')
    units = db.relationship('Unit', backref='property', lazy='dynamic')

    # Schemas
    single_schema = PropertySchema()
    many_schema = PropertySchema(many=True)
