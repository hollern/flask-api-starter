from flask import make_response
from app.routes import blueprint


@blueprint.app_errorhandler(404)
def error_404(*args, **kwargs):
    return make_response({
        'status': 'error',
        'message': 'The requested resource does not exist.'
    }, 404)


@blueprint.app_errorhandler(405)
def error_405(*args, **kwargs):
    return make_response({
        'status': 'error',
        'message': 'Method not allowed.'
    }, 405)
