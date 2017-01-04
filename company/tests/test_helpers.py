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


def test_get_employees_label_none():
    assert helpers.get_employees_label('') == ''


def test_pair_sector_values_with_label_empty():
    for value in [None, []]:
        assert helpers.pair_sector_values_with_label(value) == []


def test_get_company_profile_from_response(retrieve_profile_data):
    response = requests.Response()
    response.json = lambda: retrieve_profile_data
    expected = {
        'keywords': 'word1 word2',
        'website': 'http://example.com',
        'linkedin_url': 'http://www.linkedin.com',
        'contact_details': {
            'email_full_name': 'Jeremy',
            'address_line_1': '123 Fake Street',
            'address_line_2': 'Fakeville',
            'locality': 'London',
            'postal_code': 'E14 6XK',
            'po_box': 'abc',
            'email_address': 'test@example.com',
            'country': 'GB',
            'postal_full_name': 'Jeremy',
        },
        'supplier_case_studies': [],
        'sectors': [{'label': 'Security', 'value': 'SECURITY'}],
        'name': 'Great company',
        'twitter_url': 'http://www.twitter.com',
        'verified_with_code': True,
        'date_of_creation': datetime(2015, 3, 2, 0, 0),
        'logo': 'nice.jpg',
        'facebook_url': 'http://www.facebook.com',
        'is_address_set': True,
        'employees': '501-1,000',
        'has_social_links': True,
        'number': '01234567',
        'description': 'Ecommerce website',
        'modified': datetime(2016, 11, 23, 11, 21, 10, 977518),
    }

    actual = helpers.get_company_profile_from_response(response)
    assert actual == expected


def test_format_case_study():
    case_study = {
        'sector': 'AEROSPACE',
    }
    expected = {
        'sector': {
            'label': 'Aerospace'
        }
    }
    actual = helpers.format_case_study(case_study)
    assert actual == expected


def test_get_public_company_profile_from_response(retrieve_profile_data):
    response = requests.Response()
    response.json = lambda: retrieve_profile_data
    expected = {
        'twitter_url': 'http://www.twitter.com',
        'contact_details': {
            'po_box': 'abc',
            'address_line_2': 'Fakeville',
            'address_line_1': '123 Fake Street',
            'email_full_name': 'Jeremy',
            'country': 'GB',
            'email_address': 'test@example.com',
            'postal_code': 'E14 6XK',
            'locality': 'London',
            'postal_full_name': 'Jeremy',
        },
        'verified_with_code': True,
        'facebook_url': 'http://www.facebook.com',
        'is_address_set': True,
        'has_social_links': True,
        'website': 'http://example.com',
        'sectors': [{'value': 'SECURITY', 'label': 'Security'}],
        'number': '01234567',
        'supplier_case_studies': [],
        'date_of_creation': datetime(2015, 3, 2, 0, 0),
        'logo': 'nice.jpg',
        'modified': datetime(2016, 11, 23, 11, 21, 10, 977518),
        'description': 'Ecommerce website',
        'linkedin_url': 'http://www.linkedin.com',
        'employees': '501-1,000',
        'keywords': 'word1 word2',
        'name': 'Great company',
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
                'keywords': 'word1 word2',
                'contact_details': {
                    'email_full_name': 'Jeremy',
                    'locality': 'London',
                    'country': 'GB',
                    'address_line_2': 'Fakeville',
                    'address_line_1': '123 Fake Street',
                    'po_box': 'abc',
                    'postal_code': 'E14 6XK',
                    'email_address': 'test@example.com',
                    'postal_full_name': 'Jeremy',
                },
                'employees': '501-1,000',
                'number': '01234567',
                'supplier_case_studies': [],
                'verified_with_code': True,
                'website': 'http://example.com',
                'facebook_url': 'http://www.facebook.com',
                'linkedin_url': 'http://www.linkedin.com',
                'name': 'Great company',
                'is_address_set': True,
                'twitter_url': 'http://www.twitter.com',
                'sectors': [
                    {
                        'label': 'Security',
                        'value': 'SECURITY'
                    }
                ],
                'has_social_links': True,
                'description': 'Ecommerce website',
                'modified': datetime(2016, 11, 23, 11, 21, 10, 977518),
                'date_of_creation': datetime(2015, 3, 2, 0, 0)}
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
            'linkedin_url': 'http://www.linkedin.com',
            'logo': 'nice.jpg',
            'name': 'Great company',
            'sectors': [{'value': 'SECURITY', 'label': 'Security'}],
            'is_address_set': True,
            'facebook_url': 'http://www.facebook.com',
            'twitter_url': 'http://www.twitter.com',
            'keywords': 'word1 word2',
            'number': '01234567',
            'date_of_creation': datetime(2015, 3, 2, 0, 0),
            'website': 'http://example.com',
            'modified': datetime(2016, 11, 23, 11, 21, 10, 977518),
            'supplier_case_studies': [],
            'has_social_links': True,
            'contact_details': {
                'postal_code': 'E14 6XK',
                'locality': 'London',
                'email_address': 'test@example.com',
                'po_box': 'abc',
                'postal_full_name': 'Jeremy',
                'country': 'GB',
                'address_line_2': 'Fakeville',
                'email_full_name': 'Jeremy',
                'address_line_1': '123 Fake Street',
            },
            'verified_with_code': True,
            'employees': '501-1,000',
        },
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


def test_format_company_details_address_set(retrieve_profile_data):
    retrieve_profile_data['contact_details'] = {'key': 'value'}
    actual = helpers.format_company_details(retrieve_profile_data)

    assert actual['is_address_set'] is True


def test_format_company_details_address_not_set(retrieve_profile_data):
    retrieve_profile_data['contact_details'] = {}
    actual = helpers.format_company_details(retrieve_profile_data)

    assert actual['is_address_set'] is False


def test_format_company_details_none_address_not_set(retrieve_profile_data):
    retrieve_profile_data['contact_details'] = None
    actual = helpers.format_company_details(retrieve_profile_data)

    assert actual['is_address_set'] is False
