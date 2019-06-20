import http
from unittest.mock import call, patch, Mock
from unittest import mock

import pytest
import requests

from django.core.urlresolvers import reverse, NoReverseMatch

from core.helpers import CompanyParser
from core.tests.helpers import create_response
from directory_api_client.client import api_client
from find_a_supplier import helpers, views


@pytest.fixture()
def mock_retrieve_company_non_find_a_supplier(retrieve_profile_data):
    retrieve_profile_data['is_published_find_a_supplier'] = False
    patch = mock.patch.object(
        api_client.company, 'retrieve_public_profile',
        return_value=create_response(200, retrieve_profile_data)
    )
    yield patch.start()
    patch.stop()


def test_public_profile_different_slug_redirected(
    client, retrieve_profile_data
):
    url = reverse(
        'find-a-supplier:profile',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug'] + 'thing',
        }
    )
    expected_redirect_url = reverse(
        'find-a-supplier:profile',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug'],
        }
    )

    response = client.get(url)

    assert response.status_code == 302
    assert response.get('Location') == expected_redirect_url


def test_public_profile_missing_slug_redirected(client, retrieve_profile_data):
    url = reverse(
        'find-a-supplier:profile-slugless',
        kwargs={
            'company_number': retrieve_profile_data['number'],
        }
    )
    expected_redirect_url = reverse(
        'find-a-supplier:profile',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug'],
        }
    )

    response = client.get(url)

    assert response.status_code == 302
    assert response.get('Location') == expected_redirect_url


def test_public_profile_same_slug_not_redirected(
    client, retrieve_profile_data
):
    url = reverse(
        'find-a-supplier:profile',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug'],
        }
    )

    response = client.get(url)
    assert response.status_code == http.client.OK


def test_public_profile_details_verbose_context(client, retrieve_profile_data):
    url = reverse(
        'find-a-supplier:profile',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug'],
        }
    )
    response = client.get(url + '?verbose=true')
    assert response.status_code == http.client.OK
    assert response.context_data['show_description'] is True


def test_public_profile_details_non_verbose_context(
    client, retrieve_profile_data
):
    url = reverse(
        'find-a-supplier:profile',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug'],
        }
    )
    response = client.get(url)
    assert response.status_code == http.client.OK
    assert response.context_data['show_description'] is False


@patch.object(views.api_client.company, 'retrieve_public_profile', Mock)
@patch('core.helpers.get_company_profile')
def test_public_profile_details_exposes_context(
    mock_get_company_profile, client, retrieve_profile_data
):
    mock_get_company_profile.return_value = retrieve_profile_data
    url = reverse(
        'find-a-supplier:profile',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug']
        },
    )
    response = client.get(url)
    assert response.status_code == http.client.OK
    assert response.template_name == [
        views.ProfileView.template_name
    ]
    assert response.context_data['company'] == (
        CompanyParser(retrieve_profile_data).serialize_for_template()
    )
    assert response.context_data['social'] == {
        'description': retrieve_profile_data['summary'],
        'image': retrieve_profile_data['logo'],
        'title': (
            f'International trade profile: {retrieve_profile_data["name"]}'
        )
    }


def test_company_profile_list_with_params_redirects_to_search(client):
    url = reverse('find-a-supplier:public-company-profiles-list')
    response = client.get(url, {'sectors': 'AEROSPACE'})

    assert response.status_code == 302
    assert response.get('Location') == '/trade/search/?sector=AEROSPACE'


def test_company_profile_list_redirects_to_search(client):
    url = reverse('find-a-supplier:public-company-profiles-list')
    response = client.get(url)

    assert response.status_code == 302
    assert response.get('Location') == '/trade/search/'


@patch('core.helpers.get_company_profile')
def test_public_profile_details_calls_api(
    mock_retrieve_profile, client, retrieve_profile_data
):
    mock_retrieve_profile.return_value = retrieve_profile_data
    url = reverse(
        'find-a-supplier:profile',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug'],
        }
    )
    client.get(url)

    assert mock_retrieve_profile.call_count == 1
    assert mock_retrieve_profile.call_args == call(
        retrieve_profile_data['number']
    )


@patch.object(views.api_client.company, 'retrieve_public_profile')
def test_public_profile_details_handles_bad_status(
    mock_retrieve_public_profile, client, api_response_400
):
    mock_retrieve_public_profile.return_value = api_response_400
    url = reverse(
        'find-a-supplier:profile',
        kwargs={'company_number': '01234567', 'slug': 'thing'}
    )

    with pytest.raises(requests.exceptions.HTTPError):
        client.get(url)


@patch.object(views.api_client.company, 'retrieve_public_profile')
def test_public_profile_details_handles_404(
    mock_retrieve_public_profile, client, api_response_404
):
    mock_retrieve_public_profile.return_value = api_response_404
    url = reverse(
        'find-a-supplier:profile',
        kwargs={'company_number': '01234567', 'slug': 'thing'}
    )

    response = client.get(url)

    assert response.status_code == http.client.NOT_FOUND


def test_public_profile_details_404_non_fas(
        mock_retrieve_company_non_find_a_supplier,
        client,
        retrieve_profile_data,
):
    url = reverse(
        'find-a-supplier:profile',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug'],
        }
    )

    response = client.get(url)

    assert response.status_code == 404


@patch.object(views.api_client.company, 'retrieve_public_case_study')
def test_supplier_case_study_exposes_context(
    mock_retrieve_public_case_study, client, supplier_case_study_data,
    api_response_retrieve_public_case_study_200
):
    mock_retrieve_public_case_study.return_value = (
        api_response_retrieve_public_case_study_200
    )
    expected_case_study = helpers.get_case_study_details_from_response(
        api_response_retrieve_public_case_study_200
    )
    url = reverse(
        'case-study-details',
        kwargs={
            'id': supplier_case_study_data['pk'],
            'slug': supplier_case_study_data['slug'],
        }
    )
    response = client.get(url)

    assert response.status_code == http.client.OK
    assert response.template_name == [
        views.CaseStudyDetailView.template_name
    ]
    assert response.context_data['case_study'] == expected_case_study
    assert response.context_data['social'] == {
        'description': expected_case_study['description'],
        'image': expected_case_study['image_one'],
        'title': 'Project: {}'.format(expected_case_study['title']),
    }


@patch.object(views.api_client.company, 'retrieve_public_case_study')
def test_supplier_case_study_calls_api(
    mock_retrieve_public_case_study, client, supplier_case_study_data,
    api_response_retrieve_public_case_study_200
):
    mock_retrieve_public_case_study.return_value = (
        api_response_retrieve_public_case_study_200
    )
    url = reverse(
        'case-study-details',
        kwargs={
            'id': supplier_case_study_data['pk'],
            'slug': supplier_case_study_data['slug'],
        }
    )

    client.get(url)

    assert mock_retrieve_public_case_study.call_count == 1
    assert mock_retrieve_public_case_study.call_args == call('2')


def test_case_study_different_slug_redirected(
    supplier_case_study_data, client
):
    url = reverse(
        'case-study-details',
        kwargs={
            'id': supplier_case_study_data['pk'],
            'slug': supplier_case_study_data['slug'] + 'thing',
        }
    )
    expected_redirect_url = reverse(
        'case-study-details',
        kwargs={
            'id': supplier_case_study_data['pk'],
            'slug': supplier_case_study_data['slug'],
        }
    )

    response = client.get(url)

    assert response.status_code == 302
    assert response.get('Location') == expected_redirect_url


def test_case_study_missing_slug_redirected(supplier_case_study_data, client):
    url = reverse(
        'case-study-details-slugless',
        kwargs={
            'id': supplier_case_study_data['pk'],
        }
    )
    expected_redirect_url = reverse(
        'case-study-details',
        kwargs={
            'id': supplier_case_study_data['pk'],
            'slug': supplier_case_study_data['slug'],
        }
    )

    response = client.get(url)

    assert response.status_code == 302
    assert response.get('Location') == expected_redirect_url


def test_case_study_same_slug_not_redirected(supplier_case_study_data, client):
    url = reverse(
        'case-study-details',
        kwargs={
            'id': supplier_case_study_data['pk'],
            'slug': supplier_case_study_data['slug'],
        }
    )

    response = client.get(url)
    assert response.status_code == http.client.OK


@patch.object(views.api_client.company, 'retrieve_public_case_study')
def test_supplier_case_study_handles_bad_status(
    mock_retrieve_public_case_study, client, api_response_400,
    supplier_case_study_data
):
    mock_retrieve_public_case_study.return_value = api_response_400
    url = reverse(
        'case-study-details',
        kwargs={
            'id': supplier_case_study_data['pk'],
            'slug': supplier_case_study_data['slug'],
        }
    )

    with pytest.raises(requests.exceptions.HTTPError):
        client.get(url)


@patch.object(views.api_client.company, 'retrieve_public_case_study')
def test_supplier_case_study_handles_404(
    mock_retrieve_public_case_study, client, api_response_404,
    supplier_case_study_data
):
    mock_retrieve_public_case_study.return_value = api_response_404
    url = reverse(
        'case-study-details',
        kwargs={
            'id': supplier_case_study_data['pk'],
            'slug': supplier_case_study_data['slug'],
        }
    )
    response = client.get(url)

    assert response.status_code == http.client.NOT_FOUND


def test_contact_company_view(client, retrieve_profile_data):
    url = reverse(
        'find-a-supplier:company-contact',
        kwargs={'company_number': retrieve_profile_data['number']},
    )
    response = client.get(url)

    assert response.status_code == http.client.OK


@patch.object(views.ContactCompanyView.form_class, 'save')
def test_contact_company_view_feature_submit_forms_api_success(
    mock_save, client, valid_contact_company_data, retrieve_profile_data,
    settings
):

    url = reverse(
        'find-a-supplier:company-contact',
        kwargs={
            'company_number': retrieve_profile_data['number'],
        },
    )
    response = client.post(url, valid_contact_company_data)

    assert response.status_code == 302
    assert response.url == reverse(
        'find-a-supplier:company-contact-sent',
        kwargs={'company_number': retrieve_profile_data['number']}
    ) + '?'
    assert mock_save.call_count == 1
    assert mock_save.call_args == call(
        email_address=retrieve_profile_data['email_address'],
        form_url=url,
        sender={
            'email_address': valid_contact_company_data['email_address'],
            'country_code': valid_contact_company_data['country'],
        },
        spam_control={'contents': ['greetings', 'and salutations']},
        template_id=settings.CONTACT_FAS_COMPANY_NOTIFY_TEMPLATE_ID,
    )


@patch.object(views.ContactCompanyView.form_class.action_class, 'save')
def test_contact_company_view_feature_submit_api_forms_failure(
    mock_save, api_response_400, client,
    valid_contact_company_data, retrieve_profile_data,
):
    mock_save.return_value = api_response_400
    url = reverse(
        'find-a-supplier:company-contact',
        kwargs={
            'company_number': retrieve_profile_data['number'],
        },
    )
    with pytest.raises(requests.exceptions.HTTPError):
        client.post(url, valid_contact_company_data)


@patch.object(views.api_client.company, 'retrieve_public_profile', Mock)
@patch('core.helpers.get_company_profile')
def test_contact_company_exposes_context(mock_get_company_profile, client):
    mock_get_company_profile.return_value = data = {
        'number': '01234567',
        'slug': 'thing',
        'is_published_find_a_supplier': True,
        'company_type': 'COMPANIES_HOUSE',
    }
    url = reverse(
        'find-a-supplier:company-contact',
        kwargs={'company_number': '01234567'}
    )

    response = client.get(url)
    assert response.status_code == http.client.OK
    assert response.template_name == [views.ContactCompanyView.template_name]
    assert response.context_data['company'] == (
        CompanyParser(data).serialize_for_template()
    )


@patch('find_a_supplier.views.CompanySearchView.get_results_and_count')
def test_company_search_submit_form_on_get(
    mock_get_results_and_count, client, search_results
):
    results = [{'number': '1234567', 'slug': 'thing'}]
    mock_get_results_and_count.return_value = (results, 20)

    response = client.get(reverse('find-a-supplier:search'), {'q': '123'})

    assert response.status_code == 200
    assert response.context_data['results'] == results


def test_company_search_redirects_using_term(client):

    url = reverse('find-a-supplier:search')
    response = client.get(url, {'term': '123'})

    assert response.status_code == 302
    assert response.url == url + '?q=123'


@patch('find_a_supplier.views.CompanySearchView.get_results_and_count')
def test_company_search_pagination_count(
    mock_get_results_and_count, client, search_results
):
    results = [{'number': '1234567', 'slug': 'thing'}]
    mock_get_results_and_count.return_value = (results, 20)

    response = client.get(reverse('find-a-supplier:search'), {'q': '123'})

    assert response.status_code == 200
    assert response.context_data['pagination'].paginator.count == 20


@patch('directory_api_client.client.api_client.company.search_company')
def test_company_search_pagination_param(
    mock_search, client, search_results, api_response_search_200
):
    mock_search.return_value = api_response_search_200

    url = reverse('find-a-supplier:search')
    response = client.get(
        url, {'q': '123', 'page': 1, 'sectors': ['AEROSPACE']}
    )

    assert response.status_code == 200
    assert mock_search.call_count == 1
    assert mock_search.call_args == call(
        page=1, size=10, term='123', sectors=['AEROSPACE'],
    )


@patch('directory_api_client.client.api_client.company.search_company')
def test_company_search_sector_empty(
    mock_search, client, search_results, api_response_search_200
):
    mock_search.return_value = api_response_search_200

    url = reverse('find-a-supplier:search')
    response = client.get(
        url, {'q': '123', 'page': 1, 'sectors': ''}
    )
    assert response.status_code == 200
    assert mock_search.call_count == 1
    assert mock_search.call_args == call(
        page=1, size=10, term='123', sectors=[],
    )


@patch('directory_api_client.client.api_client.company.search_company')
def test_company_search_pagination_empty_page(
    mock_search, client, search_results, api_response_search_200
):
    mock_search.return_value = api_response_search_200

    url = reverse('find-a-supplier:search')
    response = client.get(url, {'q': '123', 'page': 100})

    assert response.status_code == 302
    assert response.get('Location') == '/trade/search/?q=123'


@patch('find_a_supplier.views.CompanySearchView.get_results_and_count')
def test_company_search_not_submit_without_params(
    mock_get_results_and_count, client
):
    response = client.get(reverse('find-a-supplier:search'))

    assert response.status_code == 200
    mock_get_results_and_count.assert_not_called()


@patch('directory_api_client.client.api_client.company.search_company')
def test_company_search_api_call_error(mock_search, api_response_400, client):
    mock_search.return_value = api_response_400

    with pytest.raises(requests.exceptions.HTTPError):
        client.get(reverse('find-a-supplier:search'), {'q': '123'})


@patch('directory_api_client.client.api_client.company.search_company')
@patch.object(views, 'get_results_from_search_response')
def test_company_search_api_success(
    mock_get_results_from_search_response, mock_search,
    api_response_search_200, client
):
    mock_search.return_value = api_response_search_200
    mock_get_results_from_search_response.return_value = {
        'results': [],
        'hits': {'total': 2}
    }
    response = client.get(reverse('find-a-supplier:search'), {'q': '123'})

    assert response.status_code == 200
    assert mock_get_results_from_search_response.call_count == 1
    assert mock_get_results_from_search_response.call_args == call(
        api_response_search_200
    )


@patch('directory_api_client.client.api_client.company.search_company')
def test_company_search_response_no_highlight(
    mock_search, api_response_search_200, client
):
    mock_search.return_value = api_response_search_200

    response = client.get(reverse('find-a-supplier:search'), {'q': 'wolf'})

    assert b'this is a short summary' in response.content


@patch('directory_api_client.client.api_client.company.search_company')
def test_company_highlight_description(
    mock_search, api_response_search_description_highlight_200, client
):
    mock_search.return_value = api_response_search_description_highlight_200

    response = client.get(reverse('find-a-supplier:search'), {'q': 'wolf'})
    expected = (
        b'<em>wolf</em> in sheep clothing description...'
        b'to the max <em>wolf</em>.'
    )

    assert expected in response.content


@patch('directory_api_client.client.api_client.company.search_company')
def test_company_search_highlight_summary(
    mock_search, api_response_search_summary_highlight_200, client
):
    mock_search.return_value = api_response_search_summary_highlight_200

    response = client.get(reverse('find-a-supplier:search'), {'q': 'wolf'})

    assert b'<em>wolf</em> in sheep clothing summary.' in response.content


@pytest.mark.parametrize('name,number,slug', [
    ['find-a-supplier:profile', '01234567',   'a'],
    ['find-a-supplier:profile', 'SC01234567', 'a'],
    ['find-a-supplier:profile-slugless', '01234567', None],
    ['find-a-supplier:profile-slugless', 'SC01234567', None],
    ['find-a-supplier:company-contact', '01234567', None],
    ['find-a-supplier:company-contact', 'SC01234567', None],
])
def test_company_profile_url_routing_200(name, number, slug):
    kwargs = {'company_number': number}
    if slug:
        kwargs['slug'] = slug

    assert reverse(name, kwargs=kwargs)


@pytest.mark.parametrize('name,number,slug', [
    ['find-a-supplier:profile',          '.', 'a'],
    ['find-a-supplier:profile-slugless', '.', None],
    ['find-a-supplier:company-contact', '.', 'a'],
])
def test_company_profile_url_routing_404(name, number, slug):
    kwargs = {'company_number': number}
    if slug:
        kwargs['slug'] = slug

    with pytest.raises(NoReverseMatch):
        assert reverse(name, kwargs=kwargs)


def test_contact_company_sent(client):
    url = reverse(
        'find-a-supplier:company-contact-sent',
        kwargs={'company_number': '01111111'}
    )
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [
        views.ContactCompanySentView.template_name
    ]


@pytest.mark.parametrize('params', [
    {'show-guide': True},
    {'q': '', 'sectors': ''},
    {'q': ''},
    {'sectors': ''},
])
def test_home_page_show_guide(client, params):
    url = reverse('find-a-supplier:search')

    response = client.get(url, params)

    assert response.status_code == 200
    assert response.context_data['show_search_guide'] is True


@pytest.mark.parametrize('params', [
    {'q': 'foo', 'sectors': 'bar'},
    {'q': 'bar'},
    {'sectors': 'foo'},
    {}
])
@mock.patch.object(views.CompanySearchView, 'get_results_and_count')
def test_home_page_hide_guide(mock_get_results_and_count, client, params):
    results = [{'number': '1234567', 'slug': 'thing'}]
    mock_get_results_and_count.return_value = (results, 20)

    url = reverse('find-a-supplier:search')

    response = client.get(url, params)

    assert response.status_code == 200
    assert response.context_data['show_search_guide'] is False
