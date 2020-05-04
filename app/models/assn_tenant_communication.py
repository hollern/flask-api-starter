from app import db

from sqlalchemy.dialects.postgresql import UUID

communications_with_tenants = db.Table(
    'communications_with_tenants',
    db.Column('linked_tenant', UUID(as_uuid=True), db.ForeignKey('tenants.id'), index=True, nullable=False),
    db.Column('linked_communication', UUID(as_uuid=True), db.ForeignKey('communications.id'), index=True, nullable=False)
)
