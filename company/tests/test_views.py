import http
from unittest.mock import patch, Mock

from directory_validators.constants import choices
import pytest
import requests

from django.core.urlresolvers import reverse

from company import helpers, views


@pytest.fixture
def api_response_200():
    response = requests.Response()
    response.status_code = http.client.OK
    return response


@pytest.fixture
def api_response_400():
    response = requests.Response()
    response.status_code = http.client.BAD_REQUEST
    return response


@pytest.fixture
def api_response_404(*args, **kwargs):
    response = requests.Response()
    response.status_code = http.client.NOT_FOUND
    return response


@pytest.fixture
def retrieve_supplier_case_study_200(api_response_200):
    response = api_response_200
    response.json = lambda: {'field': 'value'}
    return response


@patch.object(views.api_client.company,
              'retrieve_public_profile_by_companies_house_number', Mock)
@patch.object(helpers, 'get_public_company_profile_from_response')
def test_public_company_profile_details_exposes_context(
    mock_get_public_company_profile_from_response, client
):
    mock_get_public_company_profile_from_response.return_value = {}
    url = reverse(
        'public-company-profiles-detail', kwargs={'company_number': '01234567'}
    )
    response = client.get(url)
    assert response.status_code == http.client.OK
    assert response.template_name == [
        views.PublicProfileDetailView.template_name
    ]
    assert response.context_data['company'] == {}
    assert response.context_data['show_edit_links'] is False


def test_company_profile_list_exposes_context(
    client, api_response_list_public_profile_200
):
    url = reverse('public-company-profiles-list')
    params = {'sectors': choices.COMPANY_CLASSIFICATIONS[1][0]}
    expected_companies = helpers.get_company_list_from_response(
        api_response_list_public_profile_200
    )['results']

    response = client.get(url, params)

    assert response.status_code == http.client.OK
    assert response.template_name == views.PublicProfileListView.template_name
    assert response.context_data['companies'] == expected_companies
    assert response.context_data['pagination'].paginator.count == 20


@patch.object(helpers, 'get_public_company_profile_from_response')
@patch.object(views.api_client.company,
              'retrieve_public_profile_by_companies_house_number')
def test_public_company_profile_details_calls_api(
    mock_retrieve_public_profile,
    mock_get_public_company_profile_from_response, client
):
    mock_get_public_company_profile_from_response.return_value = {}
    url = reverse(
        'public-company-profiles-detail', kwargs={'company_number': '01234567'}
    )
    client.get(url)

    assert mock_retrieve_public_profile.called_once_with(1)


@patch.object(helpers, 'get_public_company_profile_from_response')
@patch.object(views.api_client.company,
              'retrieve_public_profile_by_companies_house_number')
def test_public_company_profile_details_handles_bad_status(
    mock_retrieve_public_profile,
    mock_get_public_company_profile_from_response, client, api_response_400
):
    mock_retrieve_public_profile.return_value = api_response_400
    url = reverse(
        'public-company-profiles-detail', kwargs={'company_number': '01234567'}
    )

    with pytest.raises(requests.exceptions.HTTPError):
        client.get(url)


def test_company_profile_list_exposes_selected_sector_label(client):
    url = reverse('public-company-profiles-list')
    params = {'sectors': choices.COMPANY_CLASSIFICATIONS[1][0]}
    response = client.get(url, params)

    expected_label = choices.COMPANY_CLASSIFICATIONS[1][1]
    assert response.context_data['selected_sector_label'] == expected_label


@patch.object(views.api_client.company, 'list_public_profiles')
def test_company_profile_list_calls_api(
    mock_list_public_profiles, client
):
    url = reverse('public-company-profiles-list')
    params = {'sectors': choices.COMPANY_CLASSIFICATIONS[1][0]}
    client.get(url, params)

    assert mock_list_public_profiles.called_once_with(
        sectors=choices.COMPANY_CLASSIFICATIONS[1][0],
    )


@patch.object(views.api_client.company, 'list_public_profiles')
def test_company_profile_list_handles_bad_status(
    mock_retrieve_public_profile, client, api_response_400
):
    mock_retrieve_public_profile.return_value = api_response_400
    url = reverse('public-company-profiles-list')
    params = {'sectors': choices.COMPANY_CLASSIFICATIONS[1][0]}
    with pytest.raises(requests.exceptions.HTTPError):
        client.get(url, params)


def test_company_profile_list_handles_no_form_data(client):
    url = reverse('public-company-profiles-list')
    response = client.get(url, {})

    assert response.context_data['form'].errors == {}


@patch.object(views.api_client.company, 'list_public_profiles')
def test_company_profile_list_handles_empty_page(mock_list_profiles, client):
    mock_list_profiles.return_value = api_response_404()
    url = reverse('public-company-profiles-list')
    response = client.get(url, {'sectors': 'WATER', 'page': 10})

    assert response.status_code == http.client.FOUND
    assert response.get('Location') == '{url}?sectors=WATER'.format(url=url)
