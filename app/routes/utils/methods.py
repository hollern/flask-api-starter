from app.routes.utils import QueryBuilder, ErrorHandler, Security
from flask import make_response, request
from marshmallow import ValidationError
from app.routes.utils import exceptions
from app import models

from sqlalchemy.exc import IntegrityError


def patch_single(model, resource_id, *args, **kwargs):
    try:
        # Get JSON body
        if not request.is_json:
            return make_response(*ErrorHandler.request_is_not_json_error)
        try:
            body = request.get_json()
        except Exception as e:
            return make_response(*ErrorHandler.request_missing_body_error)
        # Get current user from JWT
        user = Security.get_current_user()
        # Get entity
        entity = model.query.filter_by(id=resource_id).first()
        if entity is None:
            return make_response(*ErrorHandler.entity_does_not_exist)
        # Ensure user is authorized to access data
        is_authorized = Security.check_authorization(entity, user)
        if not is_authorized:
            return make_response(*ErrorHandler.user_not_authorized)
        # Get data from schema
        data = model.single_schema.load(body, partial=True)
        # Update data
        entity.update(data)
        return make_response({'status': 'success', 'message': 'Entity updated.'}, 200)
    except IntegrityError as e:
        return make_response(*ErrorHandler.entity_already_exists)
    except exceptions.NoUserFoundFromTokenError as e:
        return make_response(*ErrorHandler.custom_error(str(e), 400))
    except ValidationError as e:
        return make_response(*ErrorHandler.custom_error(e.messages, 400))
    except Exception as e:
        print(e)
        return make_response(*ErrorHandler.generic_error)


def get_single(model, resource_id, *args, **kwargs):
    try:
        # Get current user from JWT
        user = Security.get_current_user()
        # Get entity
        entity = model.query.filter_by(id=resource_id).first()
        if entity is None:
            return make_response(*ErrorHandler.entity_does_not_exist)
        # Ensure user is authorized to access data
        is_authorized = Security.check_authorization(entity, user)
        if not is_authorized:
            return make_response(*ErrorHandler.user_not_authorized)
        # Get data from entity
        data = model.single_schema.dump(entity)
        # Return data
        return make_response({'status': 'success', 'data': data}, 200)
    except exceptions.NoUserFoundFromTokenError as e:
        return make_response(*ErrorHandler.custom_error(str(e), 400))
    except ValidationError as e:
        return make_response(*ErrorHandler.custom_error(e.messages, 400))
    except Exception as e:
        print(e)
        return make_response(*ErrorHandler.generic_error)


def delete_single(model, resource_id, *args, **kwargs):
    try:
        # Get current user from JWT
        user = Security.get_current_user()
        # Get entity
        entity = model.query.filter_by(id=resource_id).first()
        if entity is None:
            return make_response(*ErrorHandler.entity_does_not_exist)
        # Ensure user is authorized to access data
        is_authorized = Security.check_authorization(entity, user)
        if not is_authorized:
            return make_response(*ErrorHandler.user_not_authorized)
        # Delete data
        entity.remove()
        return make_response({'status': 'success', 'message': 'Entity deleted.'}, 204)
    except exceptions.NoUserFoundFromTokenError as e:
        return make_response(*ErrorHandler.custom_error(str(e), 400))
    except ValidationError as e:
        return make_response(*ErrorHandler.custom_error(e.messages, 400))
    except Exception as e:
        print(e)
        return make_response(*ErrorHandler.generic_error)


def post_many(model, *args, **kwargs):
    try:
        # Get JSON body
        if not request.is_json:
            return make_response(*ErrorHandler.request_is_not_json_error)
        try:
            body = request.get_json()
            if type(body) is dict:
                body = [body]
        except Exception as e:
            return make_response(*ErrorHandler.request_missing_body_error)
        # Get current user from JWT
        user = Security.get_current_user()
        # Load data with schema
        data = model.many_schema.load(body)
        # Set database_tenant_id to current user database_tenant_id
        data = Security.set_database_tenant(data, user)
        # Create data
        objs = model.create(data)
        # Return message
        return make_response({
            'status': 'success',
            'message': 'Data created.',
            'data': model.many_schema.dump(objs)  # model.many_schema.dump([obj.to_dict() for obj in objs])
        }, 201)
    except IntegrityError as e:
        return make_response(*ErrorHandler.entity_already_exists)
    except exceptions.NoUserFoundFromTokenError as e:
        return make_response(*ErrorHandler.custom_error(str(e), 400))
    except ValidationError as e:
        return make_response(*ErrorHandler.custom_error(e.messages, 400))
    except Exception as e:
        print(e)
        return make_response(*ErrorHandler.generic_error)


def get_many(model, *args, **kwargs):
    try:
        # Get current user from JWT
        user = Security.get_current_user()
        # Get data from QueryBuilder
        entity_list, result_length = QueryBuilder(model=model, user=user).get_data()
        # Get data from entity list
        data = model.many_schema.dump(entity_list)
        # Return data
        return make_response({'status': 'success', 'data': data, 'result_length': result_length}, 200)
    except exceptions.QueryBuilderError as e:
        return make_response(*ErrorHandler.custom_error(str(e), 412))
    except exceptions.NoUserFoundFromTokenError as e:
        return make_response(*ErrorHandler.custom_error(str(e), 400))
    except ValidationError as e:
        return make_response(*ErrorHandler.custom_error(e.messages, 400))
    except Exception as e:
        print(e)
        return make_response(*ErrorHandler.generic_error)


def get_many_subresources(model, resource_id, subresource, *args, **kwargs):
    try:
        # Get current user from JWT
        user = Security.get_current_user()
        # Get entity
        entity = model.query.filter_by(id=resource_id).first()
        if entity is None:
            return make_response(*ErrorHandler.entity_does_not_exist)
        # Ensure user is authorized to access data
        is_authorized = Security.check_authorization(entity, user)
        if not is_authorized:
            return make_response(*ErrorHandler.user_not_authorized)
        # Handle subresource of entity
        subresource_model = getattr(models, subresource.get('model_name'))
        entity_list = getattr(entity, subresource.get('attribute_name'))
        data = subresource_model.many_schema.dump(entity_list)
        # Return data
        return make_response({'status': 'success', 'data': data}, 200)
    except exceptions.NoUserFoundFromTokenError as e:
        return make_response(*ErrorHandler.custom_error(str(e), 400))
    except ValidationError as e:
        return make_response(*ErrorHandler.custom_error(e.messages, 400))
    except Exception as e:
        print(e)
        return make_response(*ErrorHandler.generic_error)
