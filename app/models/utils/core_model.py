from datetime import datetime
from uuid import uuid4
from app import db

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.postgresql import UUID


class CoreModel(db.Model):
    __abstract__ = True

    id = db.Column(UUID(as_uuid=True), primary_key=True, index=True, nullable=False, default=uuid4)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(db.DateTime, default=datetime.utcnow)

    # Column for multitenant database
    @declared_attr
    def database_tenant_id(self):
        return db.Column(db.Integer, db.ForeignKey('DATABASE_TENANTS.id'), index=True, nullable=False)

    @classmethod
    def create(cls, data, commit=True):
        obj_list = []
        if type(data) is dict:
            obj = cls(**data)
            db.session.add(obj)
            obj_list.append(obj)
        elif type(data) is list:
            for item in data:
                obj = cls(**item)
                db.session.add(obj)
                obj_list.append(obj)
        else:
            raise TypeError('Data type must be dict or list when using "create" method.')
        if commit:
            db.session.commit()
        return obj_list

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def update(self, update_data: dict, commit=True, **kwargs):
        for attr, value in update_data.items():
            setattr(self, attr, value)
        if commit:
            self.save()
        return self

    def remove(self, commit=True):
        db.session.delete(self)
        if commit:
            db.session.commit()

    def to_dict(self):
        columns = [str(column).split('.')[-1] for column in self.__table__.columns]
        return {column: getattr(self, column) for column in columns}
