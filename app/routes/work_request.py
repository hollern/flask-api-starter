from flask_jwt_extended import jwt_required
from app.routes import blueprint
from app import models

from app.routes.utils.methods import patch_single, get_single, delete_single, post_many, get_many

base_route = '/work_request'
model = models.WorkRequest


@blueprint.route('{}/<resource_id>'.format(base_route), methods=['PATCH'])
@jwt_required
def patch_single_work_request(resource_id, *args, **kwargs):
    return patch_single(model, resource_id)


@blueprint.route('{}/<resource_id>'.format(base_route), methods=['GET'])
@jwt_required
def get_single_work_request(resource_id, *args, **kwargs):
    return get_single(model, resource_id)


@blueprint.route('{}/<resource_id>'.format(base_route), methods=['DELETE'])
@jwt_required
def delete_single_work_request(resource_id, *args, **kwargs):
    return delete_single(model, resource_id)


@blueprint.route('{}'.format(base_route), methods=['POST'])
@jwt_required
def post_many_work_request(*args, **kwargs):
    return post_many(model)


@blueprint.route('{}'.format(base_route), methods=['GET'])
@jwt_required
def get_many_work_request(*args, **kwargs):
    return get_many(model)
