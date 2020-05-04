from testing._config import Testing
import requests

# User from test_002_company
EMAIL = 'hjvhyqfrglaqjssvhw@ttirv.org'
PASSWORD = 'Test$password1'


def test_create_company_with_initial_user():
    endpoint = Testing.base_api + '/company'
    body = {
        'name': 'Company AAA',
        'email': EMAIL,
        'password': PASSWORD
    }
    resp = requests.post(endpoint, json=body)
    assert resp.status_code == 201
    assert resp.json().get('status') == 'success'
    assert resp.json().get('token') is not None

    token = resp.json().get('token')
    linked_company = resp.json().get('data').get('linked_company')
    return token, linked_company


def test_forgot_password():
    endpoint = Testing.base_api + '/user/forgot_password'
    body = {'email': EMAIL}
    resp = requests.post(endpoint, json=body)
    assert resp.status_code == 202
    assert 'Password reset email sent' in resp.json().get('message')


if __name__ == '__main__':
    token, linked_company = test_create_company_with_initial_user()
    headers = Testing.generate_request_headers(token=token)
    test_forgot_password()
