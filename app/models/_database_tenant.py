from app import db


class DatabaseTenant(db.Model):
    __tablename__ = 'DATABASE_TENANTS'
    id = db.Column(db.Integer, primary_key=True, index=True, nullable=False, autoincrement=True)

    @classmethod
    def create(cls):
        database_tenant = cls()
        db.session.add(database_tenant)
        db.session.commit()
        return database_tenant
