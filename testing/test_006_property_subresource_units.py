from testing._config import Testing
import requests

from testing.test_002_company import test_create_company_with_initial_user


def test_create_single_property():
    endpoint = Testing.base_api + '/property'
    body = [
        {
            'name': 'Property AAA',
            'zip': '43240',
            'linked_company': linked_company
        }
    ]
    resp = requests.post(endpoint, json=body, headers=headers)
    assert resp.status_code == 201
    assert len(resp.json().get('data')) == len(body)

    property_id = resp.json().get('data')[0].get('id')
    return property_id


def test_create_many_units():
    endpoint = Testing.base_api + '/unit'
    body = [
        {
            'name': '1A',
            'linked_property': property_id
        },
        {
            'name': '2A',
            'linked_property': property_id
        }
    ]
    resp = requests.post(endpoint, json=body, headers=headers)
    assert resp.status_code == 201
    assert len(resp.json().get('data')) == len(body)


def test_get_many_units_as_subresource():
    endpoint = Testing.base_api + '/property/{}/units'.format(property_id)
    resp = requests.get(endpoint, headers=headers)
    assert resp.status_code == 200
    assert len(resp.json().get('data')) == 2


if __name__ == '__main__':
    token, linked_company = test_create_company_with_initial_user()
    headers = Testing.generate_request_headers(token=token)
    property_id = test_create_single_property()
    test_create_many_units()
    test_get_many_units_as_subresource()
