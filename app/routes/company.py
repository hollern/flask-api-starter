from flask import make_response, request
from marshmallow import ValidationError
from app.routes.utils import ErrorHandler
from app.routes import blueprint
from app import models

from sqlalchemy.exc import IntegrityError

base_route = '/company'


@blueprint.route('{}'.format(base_route), methods=['POST'])
def post_company_single():
    try:
        # Get JSON body
        if not request.is_json:
            return make_response(*ErrorHandler.request_is_not_json_error)
        body = request.get_json()
        # Load data with schema
        data = models.Company.single_schema.load(body)
        # These are the keys passed in the request body that relate to the user that needs to be created for the company
        user_columns = ['email', 'password', 'is_admin']
        # Create company (this also creates the database_tenants record)
        company = models.Company.create({k: v for k, v in data.items() if k not in user_columns})
        # Create initial user for company
        user_data = {k: v for k, v in data.items() if k in user_columns}
        user_data['linked_company'] = company.id
        user_data['database_tenant_id'] = company.database_tenant_id
        user_data['is_admin'] = True
        user = models.User.from_dict(user_data)
        # Issue access token
        access_token = user.issue_access_token()
        return make_response({
            'status': 'success',
            'token': access_token,
            'data': models.User.single_schema.dump(user)
        }, 201)
    except IntegrityError as e:
        return make_response(*ErrorHandler.entity_already_exists)
    except ValidationError as e:
        return make_response(*ErrorHandler.custom_error(e.messages, 400))
    except Exception as e:
        print(e)
        return make_response(*ErrorHandler.generic_error)
