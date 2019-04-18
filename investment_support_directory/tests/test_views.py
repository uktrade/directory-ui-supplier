from unittest import mock

from directory_api_client.client import api_client
import pytest

from django.urls import reverse

from core.tests.helpers import create_response
from investment_support_directory import helpers


@pytest.fixture(autouse=True)
def mock_retrieve_company(retrieve_profile_data):
    patch = mock.patch.object(
        api_client.company, 'retrieve_public_profile',
        return_value=create_response(200, retrieve_profile_data)
    )
    yield patch.start()
    patch.stop()


@pytest.mark.parametrize('url', (
    reverse('investment-support-directory-search'),
    reverse(
        'investment-support-directory-profile',
        kwargs={'company_number': 'ST121', 'slug': 'foo'}
    )
))
def test_feature_flag(url, client, settings):
    settings.FEATURE_FLAGS['INVESTMENT_SUPPORT_DIRECTORY_ON'] = False

    response = client.get(url)

    assert response.status_code == 404


def test_profile(
    client, settings, retrieve_profile_data
):
    settings.FEATURE_FLAGS['INVESTMENT_SUPPORT_DIRECTORY_ON'] = True
    company = helpers.CompanyParser(retrieve_profile_data)

    url = reverse(
        'investment-support-directory-profile',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug'],
        }
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.context_data['company'] == company.serialize_for_template()


def test_profile_slug_redirect(client, settings, retrieve_profile_data):
    settings.FEATURE_FLAGS['INVESTMENT_SUPPORT_DIRECTORY_ON'] = True

    url = reverse(
        'investment-support-directory-profile',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': 'something',
        }
    )

    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse(
        'investment-support-directory-profile',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug'],
        }
    )


def test_profile_calls_api(
    mock_retrieve_company, client, settings, retrieve_profile_data
):
    settings.FEATURE_FLAGS['INVESTMENT_SUPPORT_DIRECTORY_ON'] = True

    url = reverse(
        'investment-support-directory-profile',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug'],
        }
    )
    response = client.get(url)

    assert response.status_code == 200
    assert mock_retrieve_company.call_count == 1
    assert mock_retrieve_company.call_args == mock.call(
        number=retrieve_profile_data['number']
    )
