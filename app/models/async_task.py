from app.models.utils import CoreModel, CoreSchema
from marshmallow import fields
from datetime import datetime
from app import db


class AsyncTaskSchema(CoreSchema):
    function_identifier = fields.String(required=True)
    queued = fields.DateTime()
    executed = fields.DateTime()
    completed = fields.DateTime()
    completion_message = fields.String()


class AsyncTask(CoreModel):
    __tablename__ = 'async_tasks'
    function_identifier = db.Column(db.String(99), nullable=False)
    queued = db.Column(db.DateTime, default=datetime.utcnow)
    executed = db.Column(db.DateTime)
    completed = db.Column(db.DateTime)
    completion_message = db.Column(db.String(299))

    # Schemas
    single_schema = AsyncTaskSchema()
    many_schema = AsyncTaskSchema(many=True)
