from testing._config import Testing
from uuid import uuid4
import requests


def test_get_company():
    resp = requests.get(endpoint)
    assert resp.status_code == 405
    assert 'Method not allowed' in resp.text
    assert resp.json().get('status') == 'error'


def test_post_company_missing_body():
    resp = requests.post(endpoint, json={})
    assert resp.status_code == 400
    assert 'Missing data for required field' in resp.text
    assert 'email' in resp.json().get('message')
    assert 'password' in resp.json().get('message')
    assert resp.json().get('status') == 'error'


def test_post_company_invalid_body():
    resp = requests.post(endpoint, json={'bad_key': 100})
    assert resp.status_code == 400
    assert 'bad_key' in resp.json().get('message')
    assert 'Unknown field' in str(resp.json().get('message').get('bad_key'))
    assert resp.json().get('status') == 'error'


def test_post_company_with_initial_user():
    company_name = str(uuid4())[:6]
    body = dict(name='Company {}'.format(company_name),
                email='test.user.1@company{}.com'.format(company_name.lower()),
                password='Test!Password123')
    resp = requests.post(endpoint, json=body)
    assert resp.status_code == 201
    assert resp.json().get('status') == 'success'
    assert 'token' in resp.json()


def test_post_company_without_initial_user():
    company_name = str(uuid4())[:6]
    body = dict(name='Company {}'.format(company_name))
    resp = requests.post(endpoint, json=body)
    assert resp.status_code == 400
    assert resp.json().get('status') == 'error'
    assert resp.json().get('message').get('email') is not None
    assert resp.json().get('message').get('password') is not None


if __name__ == '__main__':
    endpoint = Testing.base_api + '/company'
    test_get_company()
    test_post_company_missing_body()
    test_post_company_invalid_body()
    test_post_company_with_initial_user()
    test_post_company_without_initial_user()
