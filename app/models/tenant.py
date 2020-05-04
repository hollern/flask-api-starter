from werkzeug.security import generate_password_hash, check_password_hash
from app.models import communications_with_tenants, tenants_on_leases
from app.models.utils import CoreModel, CoreSchema
from marshmallow import fields
from app import db


class TenantSchema(CoreSchema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    phone_number = fields.String()
    email = fields.String()
    date_of_birth = fields.String()
    taxpayer_id = fields.String()
    emr_contact_name = fields.String()
    emr_contact_relationship = fields.String()
    emr_contact_phone = fields.String()
    emr_contact_email = fields.String()
    street_addr_line_1 = fields.String()
    street_addr_line_2 = fields.String()
    street_addr_line_3 = fields.String()
    city = fields.String()
    state = fields.String()
    zip_code = fields.String()
    country = fields.String()
    is_cosigner = fields.Boolean()


class Tenant(CoreModel):
    __tablename__ = 'tenants'
    first_name = db.Column(db.String(99), nullable=False)
    last_name = db.Column(db.String(99), nullable=False)
    phone_number = db.Column(db.String(19))
    email = db.Column(db.String(199))
    date_of_birth = db.Column(db.Date)
    taxpayer_id = db.Column(db.String(29))
    emr_contact_name = db.Column(db.String(99))
    emr_contact_relationship = db.Column(db.String(29))
    emr_contact_phone = db.Column(db.String(19))
    emr_contact_email = db.Column(db.String(199))
    street_addr_line_1 = db.Column(db.String(149))
    street_addr_line_2 = db.Column(db.String(149))
    street_addr_line_3 = db.Column(db.String(149))
    city = db.Column(db.String(149))
    state = db.Column(db.String(9))
    zip_code = db.Column(db.String(9))
    country = db.Column(db.String(99))
    is_cosigner = db.Column(db.Boolean, default=False)

    # Relationships
    payments_made = db.relationship('PaymentMade', backref='tenant', lazy='dynamic')
    work_requests = db.relationship('WorkRequest', backref='tenant', lazy='dynamic')
    leases = db.relationship('Lease', secondary=tenants_on_leases,
                             backref=db.backref('tenant', lazy='dynamic'), lazy='dynamic')
    communications = db.relationship('Communication', secondary=communications_with_tenants,
                                     backref=db.backref('tenant', lazy='dynamic'), lazy='dynamic')

    # Schemas
    single_schema = TenantSchema()
    many_schema = TenantSchema(many=True)

    def set_taxpayer_id(self, taxpayer_id):
        self.taxpayer_id = generate_password_hash(taxpayer_id)

    def check_taxpayer_id(self, taxpayer_id):
        return check_password_hash(self.taxpayer_id, taxpayer_id)

    def record_payment_made(self):
        pass
