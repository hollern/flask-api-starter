from testing._config import Testing
import requests

from testing.test_002_company import test_create_company_with_initial_user

# User from test_002_company
EMAIL = 'test.user.1@companyaaa.com'
PASSWORD = 'Test$password1'
NEW_PASSWORD = 'Test$password2'


def test_user_login():
    endpoint = Testing.base_api + '/authenticate'
    body = {'email': EMAIL, 'password': PASSWORD}
    resp = requests.post(endpoint, json=body)

    token = resp.json().get('token')
    assert token is not None
    return token


def test_change_password():
    endpoint = Testing.base_api + '/user/change_password'
    body = {'current_password': PASSWORD, 'new_password': NEW_PASSWORD}
    resp = requests.post(endpoint, json=body, headers=headers)
    assert resp.status_code == 202
    assert resp.json().get('message') == 'Password updated.'


def test_login_old_password():
    endpoint = Testing.base_api + '/authenticate'
    body = {'email': EMAIL, 'password': PASSWORD}
    resp = requests.post(endpoint, json=body)
    assert resp.status_code == 401
    assert resp.json().get('message') == 'Incorrect password for user.'


def test_login_new_password():
    endpoint = Testing.base_api + '/authenticate'
    body = {'email': EMAIL, 'password': NEW_PASSWORD}
    resp = requests.post(endpoint, json=body)
    assert resp.status_code == 201
    assert resp.json().get('token') is not None


if __name__ == '__main__':
    token, linked_company = test_create_company_with_initial_user()
    token = test_user_login()
    headers = Testing.generate_request_headers(token=token)
    test_change_password()
    test_login_old_password()
    test_login_new_password()
