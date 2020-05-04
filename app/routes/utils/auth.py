from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims
from flask import make_response, jsonify
from functools import wraps


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        is_admin = claims.get('is_admin')
        if not is_admin:
            return make_response(jsonify({
                'status': 'error',
                'message': 'User must be admin to access this resource.'
            }), 403)
        return fn(*args, **kwargs)
    return wrapper
