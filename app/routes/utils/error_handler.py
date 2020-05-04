class ErrorHandler:
    generic_error = {
        'status': 'error',
        'message': 'An unknown server error occurred.'
    }, 500
    user_not_authorized = {
        'status': 'error',
        'message': 'User is not authorized to access this resource.'
    }, 401
    request_is_not_json_error = {
        'status': 'error',
        'message': 'Missing JSON in request.'
    }, 403
    request_missing_body_error = {
        'status': 'error',
        'message': 'Missing body in request.'
    }, 403
    entity_does_not_exist = {
        'status': 'error',
        'message': 'Entity does not exist.'
    }, 404
    user_does_not_exist = {
        'status': 'error',
        'message': 'User does not exist.'
    }, 401
    incorrect_password = {
        'status': 'error',
        'message': 'Incorrect password for user.'
    }, 401
    entity_already_exists = {
        'status': 'error',
        'message': 'Attempted to create entity with attribute that already exists.'
    }, 409

    @staticmethod
    def custom_error(message, code: int) -> tuple:
        return {
            'status': 'error',
            'message': message
        }, code
