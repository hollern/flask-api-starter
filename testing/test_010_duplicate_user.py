from testing._config import Testing
import requests

# User from test_002_company
EMAIL = 'test.user.1@companyaaa.com'
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


def test_create_non_duplicate_user():
    endpoint = Testing.base_api + '/user'
    body = {
        'email': 'test.user.2@companyaaa.com',
        'password': 'Test$password2',
        'linked_company': linked_company
    }
    resp = requests.post(endpoint, json=body, headers=headers)
    assert resp.status_code == 201
    assert resp.json().get('message') == 'Data created.'


def test_login_user_2():
    endpoint = Testing.base_api + '/authenticate'
    body = {
        'email': 'test.user.2@companyaaa.com',
        'password': 'Test$password2'
    }
    resp = requests.post(endpoint, json=body)
    assert resp.status_code == 201
    assert resp.json().get('token') is not None


def test_create_duplicate_user():
    endpoint = Testing.base_api + '/user'
    body = {
        'email': 'test.user.2@companyaaa.com',
        'password': 'Test$password2',
        'linked_company': linked_company
    }
    resp = requests.post(endpoint, json=body, headers=headers)
    assert resp.status_code == 409
    assert resp.json().get('message') == 'Attempted to create entity with attribute that already exists.'


if __name__ == '__main__':
    token, linked_company = test_create_company_with_initial_user()
    headers = Testing.generate_request_headers(token=token)
    test_create_non_duplicate_user()
    test_login_user_2()
    test_create_duplicate_user()
