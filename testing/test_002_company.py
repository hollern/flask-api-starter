from testing._config import Testing
import requests


def test_create_company_with_initial_user():
    endpoint = Testing.base_api + '/company'
    company_name = 'AAA'
    body = {
        'name': 'Company {}'.format(company_name),
        'email': 'test.user.1@company{}.com'.format(company_name.lower()),
        'password': 'Test$password1'
    }
    resp = requests.post(endpoint, json=body)
    assert resp.status_code == 201
    assert resp.json().get('status') == 'success'
    assert resp.json().get('token') is not None

    token = resp.json().get('token')
    linked_company = resp.json().get('data').get('linked_company')
    return token, linked_company


def test_create_property_with_invalid_uuid():
    endpoint = Testing.base_api + '/property'
    body = {
        'name': 'Property AAA',
        'linked_company': '100'
    }
    resp = requests.post(endpoint, json=body, headers=headers)
    assert resp.status_code == 400
    assert resp.json().get('status') == 'error'
    assert 'Not a valid UUID.' in resp.text


def test_create_property():
    endpoint = Testing.base_api + '/property'
    body = {
        'name': 'Property AAA',
        'linked_company': linked_company
    }
    resp = requests.post(endpoint, json=body, headers=headers)
    assert resp.status_code == 201
    assert resp.json().get('status') == 'success'
    assert len(resp.json().get('data')) == 1

    property_id = resp.json().get('data')[0].get('id')
    return property_id


def test_get_single_property():
    endpoint = Testing.base_api + '/property/{}'.format(property_id)
    resp = requests.get(endpoint, headers=headers)
    assert resp.status_code == 200
    assert resp.json().get('data').get('id') == property_id


def test_patch_single_property():
    endpoint = Testing.base_api + '/property/{}'.format(property_id)
    body = {
        'street_addr_line_1': '12345 Test Street'
    }
    resp = requests.patch(endpoint, json=body, headers=headers)
    assert resp.status_code == 200
    resp = requests.get(endpoint, headers=headers)
    assert resp.json().get('data').get('street_addr_line_1') == body.get('street_addr_line_1')


def test_patch_single_property_with_invalid_parameter():
    endpoint = Testing.base_api + '/property/{}'.format(property_id)
    body = {
        'street_addr_line_2': '12345 Test Street',
        'this_is_my_parameter': 'test'
    }
    resp = requests.patch(endpoint, json=body, headers=headers)
    assert resp.status_code == 400
    assert 'this_is_my_parameter' and 'Unknown field' in resp.text
    resp = requests.get(endpoint, headers=headers)
    assert resp.json().get('data').get('street_addr_line_2') is None


def test_delete_single_property():
    endpoint = Testing.base_api + '/property/{}'.format(property_id)
    resp = requests.delete(endpoint, headers=headers)
    assert resp.status_code == 204
    resp = requests.get(endpoint, headers=headers)
    assert resp.status_code == 404
    assert resp.json().get('message') == 'Entity does not exist.'


if __name__ == '__main__':
    token, linked_company = test_create_company_with_initial_user()
    headers = Testing.generate_request_headers(token=token)
    test_create_property_with_invalid_uuid()
    property_id = test_create_property()
    test_get_single_property()
    test_patch_single_property()
    test_patch_single_property_with_invalid_parameter()
    test_delete_single_property()
