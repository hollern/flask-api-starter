class Testing:
    base_api = 'http://localhost:5000/api/v1'

    @staticmethod
    def run_app():
        raise NotImplemented('This method is not implemented.')

    @staticmethod
    def generate_request_headers(**kwargs) -> dict:
        headers = {'content-type': 'application/json'}

        if kwargs.get('token'):
            headers['authorization'] = 'Bearer {}'.format(kwargs.get('token'))

        return headers
