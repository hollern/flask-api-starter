from testing._config import Testing
import requests

from testing.test_002_company import test_create_company_with_initial_user


def test_create_many_property():
    endpoint = Testing.base_api + '/property'
    body = [
        {
            'name': 'Property AAA',
            'zip': '43240',
            'linked_company': linked_company
        },
        {
            'name': 'Property AAB',
            'zip': '43240',
            'linked_company': linked_company
        },
        {
            'name': 'Property AAC',
            'zip': '12345',
            'linked_company': linked_company
        },
        {
            'name': 'New Property A',
            'zip': '43082',
            'linked_company': linked_company
        },
        {
            'name': 'New Property B',
            'zip': '43082',
            'linked_company': linked_company
        }
    ]
    resp = requests.post(endpoint, json=body, headers=headers)
    assert resp.status_code == 201
    assert len(resp.json().get('data')) == len(body)


def test_invalid_field():
    endpoint = Testing.base_api + '/property'
    params = {
        'filter_fields': [
            {
                'field': 'property_name',
                'filter_type': 'eq',
                'value': 'New Property A'
            }
        ],
        'sort_fields': [
            {
                'field': 'name',
                'descending': True
            }
        ],
        'pagination': {
            'page': 0,
            'limit': 10
        }
    }
    resp = requests.get(endpoint, json=dict(query=params), headers=headers)
    assert 'Entity has no field' in resp.json().get('message')


if __name__ == '__main__':
    token, linked_company = test_create_company_with_initial_user()
    headers = Testing.generate_request_headers(token=token)
    test_create_many_property()
    test_invalid_field()
