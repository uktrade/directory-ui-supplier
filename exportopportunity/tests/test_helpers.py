from copy import deepcopy
import datetime
from unittest.mock import patch

import pytest
from requests.exceptions import HTTPError

from exportopportunity import helpers


@pytest.fixture
def api_response_showcase_case_studies_200(api_response_200):
    response = api_response_200
    response.json = lambda: deepcopy({
        'hits': {
            'total': 1,
            'hits': [
                {
                    '_source': {
                        'description': 'things',
                        'image_one_caption': 'really good',
                        'image_three_caption': 'really good',
                        'image_two_caption': 'really good',
                        'keywords': 'things and stuff',
                        'pk': 2,
                        'sector': 'AEROSPACE',
                        'short_summary': 'Is nice',
                        'slug': 'really-good',
                        'title': 'really good',
                        'company_number': '054333344',
                        'image': 'thing.jpg',
                    }
                }
            ] * 1,
        }
    })
    return response


@pytest.fixture
def search_case_study(api_response_showcase_case_studies_200):
    stub = patch(
        'api_client.api_client.company.search_case_study',
        return_value=api_response_showcase_case_studies_200,
    )
    stub.start()
    yield
    stub.stop()


@pytest.fixture
def search_company(api_response_search_200):
    stub = patch(
        'api_client.api_client.company.search_company',
        return_value=api_response_search_200,
    )
    stub.start()
    yield
    stub.stop()


@pytest.fixture
def search_company_400(api_response_400):
    stub = patch(
        'api_client.api_client.company.search_company',
        return_value=api_response_400,
    )
    stub.start()
    yield
    stub.stop()


@pytest.fixture
def search_case_study_400(api_response_400):
    stub = patch(
        'api_client.api_client.company.search_case_study',
        return_value=api_response_400,
    )
    stub.start()
    yield
    stub.stop()


def test_get_showcase_companies_400(search_company_400):
    with pytest.raises(HTTPError):
        helpers.get_showcase_companies('AEROSPACE')


def test_get_showcase_companies_200(search_company):
    companies = helpers.get_showcase_companies('AEROSPACE')

    assert companies == [
        {
            'sectors': [{'value': 'SECURITY', 'label': 'Security'}],
            'date_of_creation': datetime.datetime(2015, 3, 2, 0, 0),
            'has_social_links': True,
            'slug': 'great-company',
            'facebook_url': 'http://www.facebook.com',
            'linkedin_url': 'http://www.linkedin.com',
            'logo': 'nice.jpg',
            'public_profile_url': '/suppliers/01234567/great-company',
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


def test_get_showcase_case_studies_400(search_case_study_400):
    with pytest.raises(HTTPError):
        helpers.get_showcase_case_studies('AEROSPACE')


def test_get_showcase_case_studies_200(search_case_study):
    case_studies = helpers.get_showcase_case_studies('AEROSPACE')

    assert case_studies == [
        {
            'slug': 'really-good',
            'image_two_caption': 'really good',
            'image': 'thing.jpg',
            'sector': {
                'label': 'Aerospace',
                'value': 'AEROSPACE',
            },
            'company_number': '054333344',
            'pk': 2,
            'keywords': 'things and stuff',
            'title': 'really good',
            'image_three_caption': 'really good',
            'case_study_url': '/case-study/2/really-good',
            'image_one_caption': 'really good',
            'description': 'things',
            'short_summary': 'Is nice'
        }
    ]
