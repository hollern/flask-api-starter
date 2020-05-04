from app.models.utils import CoreModel, CoreSchema
from marshmallow import fields, validate
from datetime import datetime
from app import db


class WorkflowSchema(CoreSchema):
    TRIGGER_MODELS = [
        'PaymentMade',
        'WorkRequest',
        'PaymentDue',
        'Property',
        'Tenant',
        'Lease',
        'Unit',
        'User'
    ]
    TRIGGER_EVENTS = ['created', 'modified', 'deleted']

    workflow_title = fields.String(required=True)
    trigger_model = fields.String(required=True, validate=validate.OneOf(TRIGGER_MODELS))
    trigger_event = fields.String(required=True, validate=validate.OneOf(TRIGGER_EVENTS))
    action = fields.String(required=True)


class Workflow(CoreModel):
    __tablename__ = 'workflows'
    workflow_title = db.Column(db.String(99))
    trigger_model = db.Column(db.String(29))
    trigger_event = db.Column(db.String(29))
    action = db.Column(db.String(29))

    # Schemas
    single_schema = WorkflowSchema()
    many_schema = WorkflowSchema(many=True)


class WorkflowConditionSchema(CoreSchema):
    pass


class WorkflowCondition(CoreModel):
    pass
