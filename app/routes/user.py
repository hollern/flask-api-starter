from app.routes.utils import ErrorHandler, Security
from app.routes.utils import admin_required
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from flask import request, make_response
from app.routes import blueprint
from app import models

from sqlalchemy.exc import IntegrityError


@blueprint.route('/authenticate', methods=['POST'])
def login(*args, **kwargs):
    try:
        # Get JSON body
        if not request.is_json:
            return make_response(*ErrorHandler.request_is_not_json_error)
        body = request.get_json()
        # Ensure email and password aren't missing
        data = models.User.authentication_schema.load(body)
        # Get user
        user = models.User.query.filter_by(email=data['email']).first()
        if user is None:
            return make_response(*ErrorHandler.user_does_not_exist)
        # Validate password
        authorized = user.check_password(data['password'])
        if not authorized:
            return make_response(*ErrorHandler.incorrect_password)
        # Issue authentication token
        access_token = user.issue_access_token()
        return make_response({'status': 'success', 'token': access_token}, 201)
    except ValidationError as e:
        return make_response(*ErrorHandler.custom_error(e, 400))
    except Exception as e:
        return make_response(*ErrorHandler.generic_error)


@blueprint.route('/user/<user_id>', methods=['GET'])
@jwt_required
def get_user_single(user_id, *args, **kwargs):
    try:
        pass
    except ValidationError as e:
        return make_response(*ErrorHandler.custom_error(e, 400))
    except Exception as e:
        return make_response(*ErrorHandler.generic_error)


@blueprint.route('/user/<user_id>', methods=['PATCH'])
@jwt_required
def patch_user_single(user_id, *args, **kwargs):
    try:
        return ''
    except Exception as e:
        return make_response(*ErrorHandler.generic_error)


@blueprint.route('/user', methods=['GET'])
@admin_required
def get_user_many(*args, **kwargs):
    try:
        return ''
    except ValidationError as e:
        return make_response(*ErrorHandler.custom_error(e, 400))
    except Exception as e:
        return make_response(*ErrorHandler.generic_error)


@blueprint.route('/user', methods=['POST'])
@jwt_required
def post_user_many(*args, **kwargs):
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
        # Ensure user is admin
        if user.is_admin is False:
            return make_response(*ErrorHandler.custom_error('Not authorized to create users. Must be admin.', 401))
        # Load data with schema
        data = models.User.many_schema.load(body)
        # Set database_tenant_id to current user database_tenant_id
        data = Security.set_database_tenant(data, user)
        # Create data
        objs = models.User.create(data)
        # Return message
        return make_response({
            'status': 'success',
            'message': 'Data created.',
            'data': models.User.many_schema.dump(objs)
        }, 201)
    except IntegrityError as e:
        return make_response(*ErrorHandler.entity_already_exists)
    except ValidationError as e:
        return make_response(*ErrorHandler.custom_error(e.messages, 400))
    except Exception as e:
        print(e)
        return make_response(*ErrorHandler.generic_error)


@blueprint.route('/user/forgot_password', methods=['POST'])
def user_forgot_password():
    try:
        # Get JSON body
        if not request.is_json:
            return make_response(*ErrorHandler.request_is_not_json_error)
        body = request.get_json()
        # Get email for password reset
        email = body.get('email')
        if email is None:
            return make_response(*ErrorHandler.custom_error('Email is missing.', 400))
        # Get user
        user = models.User.query.filter_by(email=email).first()
        if user is None:
            return make_response(*ErrorHandler.user_does_not_exist)
        # Issue reset token (will be sent via email)
        current_url = '{}{}/'.format(request.host_url, blueprint.url_prefix[1:])
        mail_resp = user.issue_password_reset_token(current_url=current_url)
        return make_response({'status': 'success', 'message': 'Password reset email sent to {}'.format(email)}, 202)
    except Exception as e:
        print(e)
        return make_response(*ErrorHandler.generic_error)


@blueprint.route('/user/reset_password/<reset_token>', methods=['POST'])
def user_reset_password(reset_token):
    try:
        return make_response({'token': reset_token})
    except Exception as e:
        print(e)
        return make_response(*ErrorHandler.generic_error)


@blueprint.route('/user/change_password', methods=['POST'])
@jwt_required
def user_change_password():
    try:
        # Get JSON body
        if not request.is_json:
            return make_response(*ErrorHandler.request_is_not_json_error)
        body = request.get_json()
        # Ensure current and new passwords aren't missing
        data = models.User.change_password_schema.load(body)
        # Get user
        user = Security.get_current_user()
        if user is None:
            return make_response(*ErrorHandler.user_does_not_exist)
        # Change password
        user.change_password(data['current_password'], data['new_password'])
        return make_response({'status': 'success', 'message': 'Password updated.'}, 202)
    except models.exceptions.InvalidPasswordError as e:
        return make_response(*ErrorHandler.custom_error(str(e), 403))
    except Exception as e:
        return make_response(*ErrorHandler.generic_error)
