from datetime import datetime

import requests
import pytest

from company import helpers


@pytest.fixture
def public_companies(retrieve_profile_data):
    return {
        'count': 100,
        'results': [retrieve_profile_data]
    }


@pytest.fixture
def public_companies_empty():
    return {
        'count': 0,
        'results': []
    }


def test_get_employees_label():
    assert helpers.get_employees_label('1001-10000') == '1,001-10,000'


def test_pair_sector_values_with_label():
    values = ['AGRICULTURE_HORTICULTURE_AND_FISHERIES', 'AEROSPACE']
    expected = [
        {
            'label': 'Agriculture, horticulture and fisheries',
            'value': 'AGRICULTURE_HORTICULTURE_AND_FISHERIES',
        },
        {
            'label': 'Aerospace',
            'value': 'AEROSPACE',
        }
    ]
    assert helpers.pair_sector_values_with_label(values) == expected


def test_pair_sector_values_with_label_contains_invalid():
    values = ['AGRICULTURE_HORTICULTURE_AND_FISHERIES', 'AEROSPACE', 'DEFENCE']
    expected = [
        {
            'label': 'Agriculture, horticulture and fisheries',
            'value': 'AGRICULTURE_HORTICULTURE_AND_FISHERIES',
        },
        {
            'label': 'Aerospace',
            'value': 'AEROSPACE',
        },
    ]

    assert helpers.pair_sector_values_with_label(values) == expected


def test_get_employees_label_none():
    assert helpers.get_employees_label('') == ''


def test_pair_sector_values_with_label_empty():
    for value in [None, []]:
        assert helpers.pair_sector_values_with_label(value) == []


def test_get_company_profile_from_response(retrieve_profile_data):
    response = requests.Response()
    response.json = lambda: retrieve_profile_data
    expected = {
        'keywords': ['word1', 'word2'],
        'website': 'http://example.com',
        'linkedin_url': 'http://www.linkedin.com',
        'email_address': 'test@example.com',
        'supplier_case_studies': [],
        'sectors': [{'label': 'Security', 'value': 'SECURITY'}],
        'name': 'Great company',
        'twitter_url': 'http://www.twitter.com',
        'date_of_creation': datetime(2015, 3, 2, 0, 0),
        'logo': 'nice.jpg',
        'facebook_url': 'http://www.facebook.com',
        'employees': '501-1,000',
        'has_social_links': True,
        'is_in_companies_house': True,
        'number': '01234567',
        'description': 'Ecommerce website',
        'summary': 'this is a short summary',
        'modified': datetime(2016, 11, 23, 11, 21, 10, 977518),
        'slug': 'great-company',
        'public_profile_url': '/trade/suppliers/01234567/great-company/',
    }

    actual = helpers.get_company_profile_from_response(response)
    assert actual == expected


def test_format_case_study():
    case_study = {
        'sector': 'AEROSPACE',
        'pk': '1',
        'slug': 'good-stuff',
    }
    expected = {
        'sector': {
            'label': 'Aerospace',
            'value': 'AEROSPACE',
        },
        'pk': '1',
        'slug': 'good-stuff',
        'case_study_url': '/trade/case-study/1/good-stuff/'
    }
    actual = helpers.format_case_study(case_study)
    assert actual == expected


def test_get_public_company_profile_from_response(retrieve_profile_data):
    response = requests.Response()
    response.json = lambda: retrieve_profile_data
    expected = {
        'twitter_url': 'http://www.twitter.com',
        'email_address': 'test@example.com',
        'facebook_url': 'http://www.facebook.com',
        'has_social_links': True,
        'is_in_companies_house': True,
        'website': 'http://example.com',
        'sectors': [{'value': 'SECURITY', 'label': 'Security'}],
        'number': '01234567',
        'supplier_case_studies': [],
        'date_of_creation': datetime(2015, 3, 2, 0, 0),
        'logo': 'nice.jpg',
        'modified': datetime(2016, 11, 23, 11, 21, 10, 977518),
        'description': 'Ecommerce website',
        'summary': 'this is a short summary',
        'linkedin_url': 'http://www.linkedin.com',
        'employees': '501-1,000',
        'keywords': ['word1', 'word2'],
        'name': 'Great company',
        'slug': 'great-company',
        'public_profile_url': '/trade/suppliers/01234567/great-company/',
    }

    actual = helpers.get_public_company_profile_from_response(response)
    assert actual == expected


def test_get_company_list_from_response(public_companies):
    response = requests.Response()
    response.json = lambda: public_companies
    expected = {
        'count': 100,
        'results': [
            {
                'logo': 'nice.jpg',
                'keywords': ['word1', 'word2'],
                'email_address': 'test@example.com',
                'employees': '501-1,000',
                'number': '01234567',
                'supplier_case_studies': [],
                'website': 'http://example.com',
                'facebook_url': 'http://www.facebook.com',
                'linkedin_url': 'http://www.linkedin.com',
                'name': 'Great company',
                'twitter_url': 'http://www.twitter.com',
                'sectors': [
                    {
                        'label': 'Security',
                        'value': 'SECURITY'
                    }
                ],
                'has_social_links': True,
                'is_in_companies_house': True,
                'description': 'Ecommerce website',
                'summary': 'this is a short summary',
                'modified': datetime(2016, 11, 23, 11, 21, 10, 977518),
                'date_of_creation': datetime(2015, 3, 2, 0, 0),
                'slug': 'great-company',
                'public_profile_url': (
                    '/trade/suppliers/01234567/great-company/'
                ),
            },
        ]
    }

    actual = helpers.get_company_list_from_response(response)
    assert actual == expected


def test_get_company_list_from_response_empty(public_companies_empty):
    response = requests.Response()
    response.json = lambda: public_companies_empty
    expected = {
        'count': 0,
        'results': [],
    }
    actual = helpers.get_company_list_from_response(response)
    assert actual == expected


def test_get_case_study_details_from_response(supplier_case_study_data):
    response = requests.Response()
    response.json = lambda: supplier_case_study_data

    expected = {
        'description': 'Damn great',
        'year': '2000',
        'title': 'Two',
        'sector': {
            'value': 'SOFTWARE_AND_COMPUTER_SERVICES',
            'label': 'Software and computer services',
        },
        'testimonial': 'I found it most pleasing.',
        'keywords': 'great',
        'image_three': 'https://image_three.jpg',
        'pk': 2,
        'website': 'http://www.google.com',
        'image_two': 'https://image_two.jpg',
        'company': {
            'description': 'Ecommerce website',
            'summary': 'this is a short summary',
            'linkedin_url': 'http://www.linkedin.com',
            'logo': 'nice.jpg',
            'name': 'Great company',
            'sectors': [{'value': 'SECURITY', 'label': 'Security'}],
            'facebook_url': 'http://www.facebook.com',
            'twitter_url': 'http://www.twitter.com',
            'keywords': ['word1', 'word2'],
            'number': '01234567',
            'date_of_creation': datetime(2015, 3, 2, 0, 0),
            'website': 'http://example.com',
            'modified': datetime(2016, 11, 23, 11, 21, 10, 977518),
            'supplier_case_studies': [],
            'has_social_links': True,
            'is_in_companies_house': True,
            'email_address': 'test@example.com',
            'employees': '501-1,000',
            'slug': 'great-company',
            'public_profile_url': '/trade/suppliers/01234567/great-company/',
        },
        'slug': 'two',
        'image_one': 'https://image_one.jpg',
        'video_one': 'https://video_one.wav',
    }
    assert helpers.get_case_study_details_from_response(response) == expected


def test_get_company_profile_from_response_without_date():
    pairs = [
        ['2010-10-10', datetime(2010, 10, 10)],
        ['', ''],
        [None, None],
    ]
    for provided, expected in pairs:
        assert helpers.format_date_of_creation(provided) == expected


def test_format_company_details_handles_keywords_empty(retrieve_profile_data):
    for value in ['', None, []]:
        retrieve_profile_data['keywords'] = value

        formatted = helpers.format_company_details(retrieve_profile_data)

        assert formatted['keywords'] == []


@pytest.mark.parametrize('data,expected', (
    ({'other': ['foo', 'bar']}, ['foo', 'bar']),
    ({}, []),
))
def test_format_company_details_handles_keywords_expertise(
    retrieve_profile_data, data, expected
):
    retrieve_profile_data['keywords'] = None
    retrieve_profile_data['expertise_products_services'] = data

    formatted = helpers.format_company_details(retrieve_profile_data)

    assert formatted['keywords'] == expected


def test_get_results_from_search_response_xss(retrieve_profile_data):
    response = requests.Response()
    response.json = lambda: {
        'hits': {
            'total': 1,
            'hits': [
                {
                    '_source': retrieve_profile_data,
                    'highlight': {
                        'description': [
                            '<a onmouseover=javascript:func()>stuff</a>',
                            'to the max <em>wolf</em>.'
                        ]
                    }

                }
            ]
        }
    }

    formatted = helpers.get_results_from_search_response(response)

    assert formatted['results'][0]['highlight'] == (
        '&lt;a onmouseover=javascript:func()&gt;stuff&lt;/a&gt;...to the max '
        '<em>wolf</em>.'
    )
