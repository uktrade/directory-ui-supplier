from unittest.mock import patch

import pytest
from requests.exceptions import HTTPError

from industry import helpers
from core.helpers import CompanyParser


@pytest.fixture
def search_company_200(api_response_search_200):
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


def test_get_showcase_companies_200(search_company_200, retrieve_profile_data):
    companies = helpers.get_showcase_companies(sector='AEROSPACE')

    assert companies == [
        CompanyParser(retrieve_profile_data).serialize_for_template()
    ]
