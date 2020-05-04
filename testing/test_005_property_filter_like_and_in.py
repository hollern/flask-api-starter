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


def test_filter_by_in():
    endpoint = Testing.base_api + '/property'
    params = {
        'filter_fields': [
            {
                'field': 'name',
                'filter_type': 'in',
                'value': ['New Property A', 'New Property B']
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
    assert len(resp.json().get('data')) == 2


def test_filter_by_in_not_list_like():
    endpoint = Testing.base_api + '/property'
    params = {
        'filter_fields': [
            {
                'field': 'name',
                'filter_type': 'in',
                'value': "(New Property A', 'New Property B)"
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
    assert resp.status_code == 400
    assert 'must be list like when using' in resp.text
    assert 'filter_fields' in resp.json().get('message')


def test_filter_by_like():
    endpoint = Testing.base_api + '/property'
    params = {
        'filter_fields': [
            {
                'field': 'name',
                'filter_type': 'like',
                'value': '%New%'
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
    assert len(resp.json().get('data')) == 2


if __name__ == '__main__':
    token, linked_company = test_create_company_with_initial_user()
    headers = Testing.generate_request_headers(token=token)
    test_create_many_property()
    test_filter_by_in()
    test_filter_by_in_not_list_like()
    test_filter_by_like()
