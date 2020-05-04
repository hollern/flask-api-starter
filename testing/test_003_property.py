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
        }
    ]
    resp = requests.post(endpoint, json=body, headers=headers)
    assert resp.status_code == 201
    assert len(resp.json().get('data')) == len(body)


def test_get_many_property():
    endpoint = Testing.base_api + '/property'
    params = {
        'filter_fields': [
            {
                'field': 'zip',
                'filter_type': 'eq',
                'value': '43240'
            }
        ],
        'sort_fields': [
            {
                'field': 'name',
                'descending': False
            }
        ],
        'pagination': {
            'page': 0,
            'limit': 10
        }
    }
    resp = requests.get(endpoint, json=dict(query=params), headers=headers)
    assert len(resp.json().get('data')) == 2


def test_get_many_property_missing_filter_fields():
    endpoint = Testing.base_api + '/property'
    params = {
        'sort_fields': [
            {
                'field': 'name',
                'descending': False
            }
        ],
        'pagination': {
            'page': 0,
            'limit': 10
        }
    }
    resp = requests.get(endpoint, json=dict(query=params), headers=headers)
    assert len(resp.json().get('data')) == 3


def test_get_many_property_missing_sort_fields():
    endpoint = Testing.base_api + '/property'
    params = {
        'filter_fields': [
            {
                'field': 'zip',
                'filter_type': 'eq',
                'value': '43240'
            }
        ],
        'pagination': {
            'page': 0,
            'limit': 10
        }
    }
    resp = requests.get(endpoint, json=dict(query=params), headers=headers)
    assert len(resp.json().get('data')) == 2


def test_get_many_property_missing_pagination():
    endpoint = Testing.base_api + '/property'
    params = {
        'filter_fields': [
            {
                'field': 'zip',
                'filter_type': 'eq',
                'value': '43240'
            }
        ],
        'sort_fields': [
            {
                'field': 'name',
                'descending': False
            }
        ]
    }
    resp = requests.get(endpoint, json=dict(query=params), headers=headers)
    assert resp.status_code == 400
    assert 'Missing data for required field.' in str(resp.json().get('message').get('pagination'))


def test_pagination_single():
    endpoint = Testing.base_api + '/property'
    params = {
        'sort_fields': [
            {
                'field': 'name',
                'descending': True
            }
        ],
        'pagination': {
            'page': 0,
            'limit': 2
        }
    }
    resp = requests.get(endpoint, json=dict(query=params), headers=headers)
    assert len(resp.json().get('data')) == 2


if __name__ == '__main__':
    token, linked_company = test_create_company_with_initial_user()
    headers = Testing.generate_request_headers(token=token)
    test_create_many_property()
    test_get_many_property_missing_filter_fields()
    test_get_many_property_missing_sort_fields()
    test_pagination_single()
