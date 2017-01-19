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
def retrieve_public_case_study_200(api_response_200):
    response = api_response_200
    response.json = lambda: {'field': 'value'}
    return response


@patch.object(views.api_client.company,
              'retrieve_public_profile_by_companies_house_number', Mock)
@patch.object(helpers, 'get_public_company_profile_from_response')
def test_public_company_profile_details_verbose_context(
    mock_get_public_company_profile_from_response, client
):
    mock_get_public_company_profile_from_response.return_value = {}
    url = reverse(
        'public-company-profiles-detail', kwargs={'company_number': '01234567'}
    )
    response = client.get(url + '?verbose=true')
    assert response.status_code == http.client.OK
    assert response.context_data['show_description'] is True


@patch.object(views.api_client.company,
              'retrieve_public_profile_by_companies_house_number', Mock)
@patch.object(helpers, 'get_public_company_profile_from_response')
def test_public_company_profile_details_non_verbose_context(
    mock_get_public_company_profile_from_response, client
):
    mock_get_public_company_profile_from_response.return_value = {}
    url = reverse(
        'public-company-profiles-detail', kwargs={'company_number': '01234567'}
    )
    response = client.get(url)
    assert response.status_code == http.client.OK
    assert response.context_data['show_description'] is False


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
        views.PublishedProfileDetailView.template_name
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
    expected_template_name = views.PublishedProfileListView.template_name

    assert response.status_code == http.client.OK
    assert response.template_name == expected_template_name
    assert response.context_data['companies'] == expected_companies
    assert response.context_data['pagination'].paginator.count == 20
    assert response.context_data['show_companies_count'] is True


def test_company_profile_list_exposes_context_show_companies_count(
    client, api_response_list_public_profile_200
):
    url = reverse('public-company-profiles-list')
    params = {'sectors': choices.COMPANY_CLASSIFICATIONS[1][0]}

    response = client.get(url, params)

    assert response.status_code == http.client.OK
    assert response.context_data['show_companies_count'] is True


def test_company_profile_list_exposes_context_hide_companies_count(
    client, api_response_list_public_profile_200
):
    url = reverse('public-company-profiles-list')

    for params in [{}, {'sectors': ''}, {'sectors': ''}]:
        response = client.get(url, {})

        assert response.status_code == http.client.OK
        assert response.context_data['show_companies_count'] is False


def test_company_profile_list_general_context(client):
    view_name = 'public-company-profiles-list'
    response = client.get(reverse(view_name))

    assert response.context['active_view_name'] == view_name


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


@patch.object(helpers, 'get_public_company_profile_from_response')
@patch.object(views.api_client.company,
              'retrieve_public_profile_by_companies_house_number')
def test_public_company_profile_details_handles_404(
    mock_retrieve_public_profile,
    mock_get_public_company_profile_from_response, client, api_response_404
):
    mock_retrieve_public_profile.return_value = api_response_404
    url = reverse(
        'public-company-profiles-detail', kwargs={'company_number': '01234567'}
    )

    response = client.get(url)

    assert response.status_code == http.client.NOT_FOUND


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


@patch.object(views.api_client.company, 'retrieve_public_case_study')
def test_supplier_case_study_exposes_context(
    mock_retrieve_public_case_study, client,
    api_response_retrieve_public_case_study_200
):
    mock_retrieve_public_case_study.return_value = (
        api_response_retrieve_public_case_study_200
    )
    expected_case_study = helpers.get_case_study_details_from_response(
        api_response_retrieve_public_case_study_200
    )
    url = reverse('case-study-details', kwargs={'id': '2'})
    response = client.get(url)

    assert response.status_code == http.client.OK
    assert response.template_name == [
        views.CaseStudyDetailView.template_name
    ]
    assert response.context_data['case_study'] == expected_case_study


@patch.object(views.api_client.company, 'retrieve_public_case_study')
def test_supplier_case_study_calls_api(
    mock_retrieve_public_case_study, client,
    api_response_retrieve_public_case_study_200
):
    mock_retrieve_public_case_study.return_value = (
        api_response_retrieve_public_case_study_200
    )
    url = reverse('case-study-details', kwargs={'id': '2'})
    client.get(url)

    assert mock_retrieve_public_case_study.called_once_with(pk='2')


@patch.object(views.api_client.company, 'retrieve_public_case_study')
def test_supplier_case_study_handles_bad_status(
    mock_retrieve_public_case_study, client, api_response_400
):
    mock_retrieve_public_case_study.return_value = api_response_400
    url = reverse('case-study-details', kwargs={'id': '2'})

    with pytest.raises(requests.exceptions.HTTPError):
        client.get(url)


@patch.object(views.api_client.company, 'retrieve_public_case_study')
def test_supplier_case_study_handles_404(
    mock_retrieve_public_case_study, client, api_response_404
):
    mock_retrieve_public_case_study.return_value = api_response_404
    url = reverse('case-study-details', kwargs={'id': '2'})

    response = client.get(url)

    assert response.status_code == http.client.NOT_FOUND


def test_contact_company_view_feature_flag_off(settings, client):
    settings.FEATURE_CONTACT_COMPANY_FORM_ENABLED = False

    url = reverse('contact-company', kwargs={'company_number': '01234567'})

    response = client.get(url)

    assert response.status_code == http.client.NOT_FOUND


def test_contact_company_view_feature_flag_on(settings, client):
    settings.FEATURE_CONTACT_COMPANY_FORM_ENABLED = True

    url = reverse('contact-company', kwargs={'company_number': '01234567'})

    response = client.get(url)

    assert response.status_code == http.client.OK


def test_contact_company_view_feature_submit(settings, client):
    settings.FEATURE_CONTACT_COMPANY_FORM_ENABLED = True

    url = reverse('contact-company', kwargs={'company_number': '01234567'})
    data = {
        'full_name': 'Jim Example',
        'company_name': 'Example Corp',
        'country': 'China',
        'email_address': 'jim@example.com',
        'sector': 'AEROSPACE',
        'subject': 'greetings',
        'body': 'and salutations',
    }
    response = client.post(url, data)

    expected_template_name = views.ContactCompanyView.success_template_name

    assert response.status_code == http.client.OK
    assert response.template_name == expected_template_name
