from app.models.utils import CoreModel, CoreSchema
from marshmallow import fields
from app import db

from app.models import DatabaseTenant


class CompanySchema(CoreSchema):
    name = fields.String(required=True)
    twilio_sms_number = fields.String()

    # Fields for the creation of the initial user
    email = fields.Email(required=True, load_only=True)
    password = fields.String(required=True, load_only=True)
    is_admin = fields.Boolean(load_only=True)


class Company(CoreModel):
    __tablename__ = 'companies'
    name = db.Column(db.String(299))
    twilio_sms_number = db.Column(db.String(19))

    # SaaS Limit Used
    limit_used_properties = db.Column(db.Integer)
    limit_used_workflows = db.Column(db.Integer)
    # SaaS Limits
    limit_properties = db.Column(db.Integer)
    limit_workflows = db.Column(db.Integer)

    # Relationships
    users = db.relationship('User', backref='company', lazy='dynamic')
    properties = db.relationship('Property', backref='company', lazy='dynamic')

    # Schemas
    single_schema = CompanySchema()
    many_schema = CompanySchema(many=True)
    partial_schema = CompanySchema(partial=True)

    @classmethod
    def create(cls, data, commit=True):
        if type(data) is dict:
            database_tenant = DatabaseTenant.create()
            data['database_tenant_id'] = database_tenant.id
            obj = cls(**data)
            db.session.add(obj)
        else:
            raise TypeError('Data type must be dict when using method: create on entity: Company.')
        if commit:
            db.session.commit()
        return obj

    def set_saas_pricing_plan(self):
        pass
