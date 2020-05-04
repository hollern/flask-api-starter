from app import db

from sqlalchemy.dialects.postgresql import UUID

tenants_on_leases = db.Table(
    'tenants_on_leases',
    db.Column('linked_tenant', UUID(as_uuid=True), db.ForeignKey('tenants.id'), index=True, nullable=False),
    db.Column('linked_lease', UUID(as_uuid=True), db.ForeignKey('leases.id'), index=True, nullable=False)
)
