from flask_jwt_extended import get_jwt_identity
from app.routes.utils import exceptions
from typing import List
from app import models


class Security:
    @staticmethod
    def get_current_user() -> models.User:
        identity = get_jwt_identity()
        user = models.User.query.filter(models.User.id == identity).first()
        if user is None:
            raise exceptions.NoUserFoundFromTokenError('A valid user was not found from the token.')
        return user

    @staticmethod
    def check_authorization(data: List[object] or object, user: models.User) -> bool:
        database_tenant_id = user.database_tenant_id
        if type(data) is list:
            for item in data:
                if getattr(item, 'database_tenant_id') != database_tenant_id:
                    return False
        else:
            if getattr(data, 'database_tenant_id') != database_tenant_id:
                return False
        return True

    @staticmethod
    def set_database_tenant(data: List[dict] or dict, user: models.User):
        database_tenant_id = user.database_tenant_id
        if type(data) is list:
            for row in data:
                row['database_tenant_id'] = database_tenant_id
        elif type(data) is dict:
            data['database_tenant_id'] = database_tenant_id
        return data
