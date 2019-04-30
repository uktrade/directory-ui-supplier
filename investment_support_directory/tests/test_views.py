from unittest import mock

from directory_api_client.client import api_client
import pytest
import requests

from django.urls import reverse

from core.tests.helpers import create_response
from investment_support_directory import helpers, forms, views


@pytest.fixture(autouse=True)
def mock_retrieve_company(retrieve_profile_data):
    patch = mock.patch.object(
        api_client.company, 'retrieve_public_profile',
        return_value=create_response(200, retrieve_profile_data)
    )
    yield patch.start()
    patch.stop()


@pytest.mark.parametrize('url', (
    reverse('investment-support-directory-home'),
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


def test_home_page_context_data(client, settings):
    settings.FEATURE_FLAGS['INVESTMENT_SUPPORT_DIRECTORY_ON'] = True

    url = reverse('investment-support-directory-home')

    response = client.get(url)

    assert response.status_code == 200
    assert response.context_data['CHOICES_FINANCIAL'] == (
        forms.CHOICES_FINANCIAL
    )
    assert response.context_data['CHOICES_HUMAN_RESOURCES'] == (
        forms.CHOICES_HUMAN_RESOURCES
    )
    assert response.context_data['CHOICES_LEGAL'] == (
        forms.CHOICES_LEGAL
    )
    assert response.context_data['CHOICES_PUBLICITY'] == (
        forms.CHOICES_PUBLICITY
    )
    assert response.context_data['CHOICES_FURTHER_SERVICES'] == (
        forms.CHOICES_FURTHER_SERVICES
    )
    assert response.context_data['CHOICES_MANAGEMENT_CONSULTING'] == (
        forms.CHOICES_MANAGEMENT_CONSULTING
    )


def test_home_page_redirect(client, settings):
    settings.FEATURE_FLAGS['INVESTMENT_SUPPORT_DIRECTORY_ON'] = True

    url = reverse('investment-support-directory-home')
    expected_url = reverse('investment-support-directory-search')

    response = client.post(url, {'q': 'foo'})

    assert response.status_code == 302
    assert response.url == f'{expected_url}?q=foo'


@mock.patch.object(views.CompanySearchView, 'get_results_and_count')
def test_search_submit_form_on_get(
    mock_get_results_and_count, client, search_results, settings
):
    settings.FEATURE_FLAGS['INVESTMENT_SUPPORT_DIRECTORY_ON'] = True

    results = [{'number': '1234567', 'slug': 'thing'}]
    mock_get_results_and_count.return_value = (results, 20)

    response = client.get(
        reverse('investment-support-directory-search'), {'q': '123'}
    )

    assert response.status_code == 200
    assert response.context_data['results'] == results


@mock.patch.object(views.CompanySearchView, 'get_results_and_count')
def test_company_search_pagination_count(
    mock_get_results_and_count, client, search_results, settings
):
    settings.FEATURE_FLAGS['INVESTMENT_SUPPORT_DIRECTORY_ON'] = True

    results = [{'number': '1234567', 'slug': 'thing'}]
    mock_get_results_and_count.return_value = (results, 20)

    response = client.get(
        reverse('investment-support-directory-search'), {'q': '123'}
    )

    assert response.status_code == 200
    assert response.context_data['pagination'].paginator.count == 20


@mock.patch.object(api_client.company, 'search_investment_search_directory')
def test_company_search_pagination_param(
    mock_search, client, search_results, api_response_search_200, settings
):
    settings.FEATURE_FLAGS['INVESTMENT_SUPPORT_DIRECTORY_ON'] = True

    mock_search.return_value = api_response_search_200

    url = reverse('investment-support-directory-search')
    response = client.get(
        url, {'q': '123', 'page': 1, 'expertise_industries': ['AEROSPACE']}
    )

    assert response.status_code == 200
    assert mock_search.call_count == 1
    assert mock_search.call_args == mock.call(
        expertise_countries=[],
        expertise_financial=None,
        expertise_industries=['AEROSPACE'],
        expertise_languages=[],
        expertise_products_services=[],
        expertise_regions=[],
        page=1,
        size=10,
        term='123'
    )


@mock.patch.object(api_client.company, 'search_investment_search_directory')
def test_company_search_pagination_empty_page(
    mock_search, client, search_results, api_response_search_200, settings
):
    settings.FEATURE_FLAGS['INVESTMENT_SUPPORT_DIRECTORY_ON'] = True

    mock_search.return_value = api_response_search_200

    url = reverse('investment-support-directory-search')
    response = client.get(url, {'q': '123', 'page': 100})

    assert response.status_code == 302
    assert response.get('Location') == (
        reverse('investment-support-directory-search') + '?q=123'
    )


@mock.patch.object(views.CompanySearchView, 'get_results_and_count')
def test_company_search_not_submit_without_params(
    mock_get_results_and_count, client, settings
):
    settings.FEATURE_FLAGS['INVESTMENT_SUPPORT_DIRECTORY_ON'] = True
    response = client.get(reverse('investment-support-directory-search'))

    assert response.status_code == 200
    mock_get_results_and_count.assert_not_called()


@mock.patch.object(api_client.company, 'search_investment_search_directory')
def test_company_search_api_call_error(
    mock_search, api_response_400, client, settings
):
    settings.FEATURE_FLAGS['INVESTMENT_SUPPORT_DIRECTORY_ON'] = True

    mock_search.return_value = api_response_400

    with pytest.raises(requests.exceptions.HTTPError):
        client.get(
            reverse('investment-support-directory-search'), {'q': '123'}
        )


@mock.patch.object(api_client.company, 'search_investment_search_directory')
@mock.patch.object(helpers, 'get_results_from_search_response')
def test_company_search_api_success(
    mock_get_results_from_search_response, mock_search, settings,
    api_response_search_200, client
):
    settings.FEATURE_FLAGS['INVESTMENT_SUPPORT_DIRECTORY_ON'] = True

    mock_search.return_value = api_response_search_200
    mock_get_results_from_search_response.return_value = {
        'results': [],
        'hits': {'total': 2}
    }
    response = client.get(
        reverse('investment-support-directory-search'), {'q': '123'}
    )

    assert response.status_code == 200
    assert mock_get_results_from_search_response.call_count == 1
    assert mock_get_results_from_search_response.call_args == mock.call(
        api_response_search_200
    )


@mock.patch.object(api_client.company, 'search_investment_search_directory')
def test_company_search_response_no_highlight(
    mock_search, api_response_search_200, client, settings
):
    settings.FEATURE_FLAGS['INVESTMENT_SUPPORT_DIRECTORY_ON'] = True

    mock_search.return_value = api_response_search_200

    response = client.get(
        reverse('investment-support-directory-search'), {'q': 'wolf'}
    )

    assert b'this is a short summary' in response.content


@mock.patch.object(api_client.company, 'search_investment_search_directory')
def test_company_highlight_description(
    mock_search, api_response_search_description_highlight_200, client,
    settings
):
    settings.FEATURE_FLAGS['INVESTMENT_SUPPORT_DIRECTORY_ON'] = True

    mock_search.return_value = api_response_search_description_highlight_200

    response = client.get(
        reverse('investment-support-directory-search'), {'q': 'wolf'}
    )
    expected = (
        b'<em>wolf</em> in sheep clothing description...'
        b'to the max <em>wolf</em>.'
    )

    assert expected in response.content


@mock.patch.object(api_client.company, 'search_investment_search_directory')
def test_company_search_highlight_summary(
    mock_search, api_response_search_summary_highlight_200, client, settings
):
    settings.FEATURE_FLAGS['INVESTMENT_SUPPORT_DIRECTORY_ON'] = True

    mock_search.return_value = api_response_search_summary_highlight_200

    response = client.get(
        reverse('investment-support-directory-search'), {'q': 'wolf'}
    )

    assert b'<em>wolf</em> in sheep clothing summary.' in response.content
