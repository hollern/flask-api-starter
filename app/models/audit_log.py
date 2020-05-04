from app.models.utils import CoreModel
from datetime import datetime
from app import db

from sqlalchemy.dialects.postgresql import UUID


class AuditLog(CoreModel):
    __tablename__ = 'audit_logs'
    action = db.Column(db.String(99))                        # way in which object was changed (verb) "entity.created"
    action_type = db.Column(db.String(9))                    # CRUD "create"
    event_name = db.Column(db.String(999))                   # common name of the event to filter down to similar events
    target = db.Column(db.String(999))                       # object being changed (noun) "entity"
    when = db.Column(db.DateTime, default=datetime.utcnow)   # server time "2019-12-31 23:59:59"
    where = db.Column(db.String(999))                        # ip address, country, etc. "0.0.0.0"
    description = db.Column(db.String(999))                  # human readable description of action taken, pages, etc.
    linked_user = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=True)  # user "email@website.com"
    linked_company = db.Column(UUID(as_uuid=True), db.ForeignKey('companies.id'), nullable=False)
