import datetime
from unittest.mock import patch

import pytest
from requests.exceptions import HTTPError

from industry import helpers


@pytest.fixture
def search_company(api_response_search_200):
    stub = patch(
        'directory_api_client.client.api_client.company.search_company',
        return_value=api_response_search_200,
    )
    stub.start()
    yield
    stub.stop()


@pytest.fixture
def search_company_400(api_response_400):
    stub = patch(
        'directory_api_client.client.api_client.company.search_company',
        return_value=api_response_400,
    )
    stub.start()
    yield
    stub.stop()


def test_get_showcase_companies_400(search_company_400):
    with pytest.raises(HTTPError):
        helpers.get_showcase_companies(sector='AEROSPACE')


def test_get_showcase_companies_200(search_company):
    companies = helpers.get_showcase_companies(sector='AEROSPACE')

    assert companies == [
        {
            'sectors': [{'value': 'SECURITY', 'label': 'Security'}],
            'date_of_creation': datetime.datetime(2015, 3, 2, 0, 0),
            'has_social_links': True,
            'is_in_companies_house': True,
            'slug': 'great-company',
            'facebook_url': 'http://www.facebook.com',
            'linkedin_url': 'http://www.linkedin.com',
            'logo': 'nice.jpg',
            'public_profile_url': '/trade/suppliers/01234567/great-company/',
            'modified': datetime.datetime(2016, 11, 23, 11, 21, 10, 977518),
            'employees': '501-1,000',
            'number': '01234567',
            'name': 'Great company',
            'twitter_url': 'http://www.twitter.com',
            'summary': 'this is a short summary',
            'supplier_case_studies': [],
            'email_address': 'test@example.com',
            'website': 'http://example.com',
            'description': 'Ecommerce website',
            'keywords': ['word1', 'word2']
        }
    ]
