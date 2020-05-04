from testing._config import Testing
import requests

from testing.test_002_company import test_create_company_with_initial_user


def test_create_many_company_a_property():
    endpoint = Testing.base_api + '/property'
    body = [
        {
            'name': 'Property A1',
            'zip': '43240',
            'linked_company': company_a
        },
        {
            'name': 'Property A2',
            'zip': '43240',
            'linked_company': company_a
        }
    ]
    resp = requests.post(endpoint, json=body, headers=headers_a)
    assert resp.status_code == 201
    assert len(resp.json().get('data')) == len(body)

    property_a = resp.json().get('data')[0].get('id')
    return property_a


def test_create_many_company_b_property():
    endpoint = Testing.base_api + '/property'
    body = [
        {
            'name': 'Property B1',
            'zip': '12345',
            'linked_company': company_b
        },
        {
            'name': 'Property B2',
            'zip': '12345',
            'linked_company': company_b
        }
    ]
    resp = requests.post(endpoint, json=body, headers=headers_b)
    assert resp.status_code == 201
    assert len(resp.json().get('data')) == len(body)

    property_b = resp.json().get('data')[0].get('id')
    return property_b


def test_company_a_cant_get_many_company_b_property():
    endpoint = Testing.base_api + '/property'
    params = {
        'filter_fields': [
            {
                'field': 'name',
                'filter_type': 'like',
                'value': '%Property%A%'
            }
        ],
        'pagination': {
            'page': 0,
            'limit': 10
        }
    }
    resp = requests.get(endpoint, json=dict(query=params), headers=headers_a)
    assert len(resp.json().get('data')) == 2
    assert resp.json().get('result_length') == 2

    params = {
        'filter_fields': [
            {
                'field': 'name',
                'filter_type': 'like',
                'value': '%Property%B%'
            }
        ],
        'pagination': {
            'page': 0,
            'limit': 10
        }
    }
    resp = requests.get(endpoint, json=dict(query=params), headers=headers_a)
    assert len(resp.json().get('data')) == 0
    assert resp.json().get('result_length') == 0


def test_company_a_cant_get_single_company_b_property():
    endpoint = Testing.base_api + '/property'

    resp = requests.get(endpoint + '/{}'.format(property_a), headers=headers_a)
    assert resp.status_code == 200
    assert resp.json().get('data').get('id') == property_a

    resp = requests.get(endpoint + '/{}'.format(property_b), headers=headers_a)
    assert resp.status_code == 401
    assert resp.json().get('message') == 'User is not authorized to access this resource.'


def test_company_a_cant_patch_company_b_property():
    endpoint = Testing.base_api + '/property'
    body = {'state': 'OH'}

    resp = requests.patch(endpoint + '/{}'.format(property_a), json=body, headers=headers_a)
    assert resp.status_code == 200
    assert resp.json().get('message') == 'Entity updated.'
    resp = requests.get(endpoint + '/{}'.format(property_a), headers=headers_a)
    assert resp.json().get('data').get('state') == body['state']

    resp = requests.patch(endpoint + '/{}'.format(property_b), json=body, headers=headers_a)
    assert resp.status_code == 401
    assert resp.json().get('message') == 'User is not authorized to access this resource.'
    resp = requests.get(endpoint + '/{}'.format(property_b), headers=headers_b)
    assert resp.json().get('data').get('state') is None


def test_company_a_cant_delete_company_b_property():
    endpoint = Testing.base_api + '/property'

    resp = requests.delete(endpoint + '/{}'.format(property_a), headers=headers_a)
    assert resp.status_code == 204
    resp = requests.get(endpoint + '/{}'.format(property_a), headers=headers_a)
    assert resp.status_code == 404

    resp = requests.delete(endpoint + '/{}'.format(property_b), headers=headers_a)
    assert resp.status_code == 401
    assert resp.json().get('message') == 'User is not authorized to access this resource.'
    resp = requests.get(endpoint + '/{}'.format(property_b), headers=headers_b)
    assert resp.json().get('data').get('id') == property_b


if __name__ == '__main__':
    token_a, company_a = test_create_company_with_initial_user()
    headers_a = Testing.generate_request_headers(token=token_a)

    token_b, company_b = test_create_company_with_initial_user()
    headers_b = Testing.generate_request_headers(token=token_b)

    property_a = test_create_many_company_a_property()
    property_b = test_create_many_company_b_property()

    test_company_a_cant_get_many_company_b_property()
    test_company_a_cant_get_single_company_b_property()
    test_company_a_cant_patch_company_b_property()
    test_company_a_cant_delete_company_b_property()
