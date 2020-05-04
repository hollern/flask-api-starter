from flask_jwt_extended import jwt_required
from app.routes import blueprint
from app import models

model = models.AsyncTask


@blueprint.route('/async_task', methods=['POST'])
@jwt_required
def post_single_async_task(*args, **kwargs):
    try:
        # Connect to RabbitMQ
        pass
    except Exception as e:
        pass


@blueprint.route('/async_task/<resource_id>', methods=['PATCH'])
@jwt_required
def patch_single_async_task(resource_id, *args, **kwargs):
    pass


@blueprint.route('/async_task/<resource_id>', method=['GET'])
@jwt_required
def get_single_async_task(resource_id, *args, **kwargs):
    pass
