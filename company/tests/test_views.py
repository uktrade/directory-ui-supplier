import http
from unittest.mock import call, patch, Mock

import pytest
import requests

from django.core.urlresolvers import reverse, NoReverseMatch

from company import helpers, views


@pytest.fixture
def api_response_200():
    response = requests.Response()
    response.status_code = http.client.OK
    return response


@pytest.fixture
def api_response_404(*args, **kwargs):
    response = requests.Response()
    response.status_code = http.client.NOT_FOUND
    return response


@pytest.fixture
def api_response_search_description_highlight_200(
    api_response_200, search_results
):
    search_results['hits']['hits'][0]['highlight'] = {
        'description': [
            '<em>wolf</em> in sheep clothing description',
            'to the max <em>wolf</em>.'
        ]
    }
    api_response_200.json = lambda: search_results
    return api_response_200


@pytest.fixture
def api_response_search_summary_highlight_200(
    api_response_200, search_results
):
    search_results['hits']['hits'][0]['highlight'] = {
        'summary': ['<em>wolf</em> in sheep clothing summary.']
    }
    api_response_200.json = lambda: search_results
    return api_response_200


def test_public_profile_different_slug_redirected(
    client, retrieve_profile_data
):
    url = reverse(
        'public-company-profiles-detail',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug'] + 'thing',
        }
    )
    expected_redirect_url = reverse(
        'public-company-profiles-detail',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug'],
        }
    )

    response = client.get(url)

    assert response.status_code == http.client.MOVED_PERMANENTLY
    assert response.get('Location') == expected_redirect_url


def test_public_profile_missing_slug_redirected(client, retrieve_profile_data):
    url = reverse(
        'public-company-profiles-detail-slugless',
        kwargs={
            'company_number': retrieve_profile_data['number'],
        }
    )
    expected_redirect_url = reverse(
        'public-company-profiles-detail',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug'],
        }
    )

    response = client.get(url)

    assert response.status_code == http.client.MOVED_PERMANENTLY
    assert response.get('Location') == expected_redirect_url


def test_public_profile_same_slug_not_redirected(
    client, retrieve_profile_data
):
    url = reverse(
        'public-company-profiles-detail',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug'],
        }
    )

    response = client.get(url)
    assert response.status_code == http.client.OK


def test_public_profile_details_verbose_context(client, retrieve_profile_data):
    url = reverse(
        'public-company-profiles-detail',
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
        'public-company-profiles-detail',
        kwargs={
            'company_number': retrieve_profile_data['number'],
            'slug': retrieve_profile_data['slug'],
        }
    )
    response = client.get(url)
    assert response.status_code == http.client.OK
    assert response.context_data['show_description'] is False


@patch.object(views.api_client.company, 'retrieve_public_profile', Mock)
@patch.object(helpers, 'get_public_company_profile_from_response')
def test_public_profile_details_exposes_context(
    mock_get_public_company_profile_from_response, client
):
    company = {
        'name': 'Example corp',
        'logo': 'logo.png',
        'summary': 'summary summary',
        'slug': 'thing',
    }
    mock_get_public_company_profile_from_response.return_value = company
    url = reverse(
        'public-company-profiles-detail',
        kwargs={'company_number': '01234567', 'slug': 'thing'},
    )
    response = client.get(url)
    assert response.status_code == http.client.OK
    assert response.template_name == [
        views.PublishedProfileDetailView.template_name
    ]
    assert response.context_data['company'] == company
    assert response.context_data['social'] == {
        'description': company['summary'],
        'image': company['logo'],
        'title': 'International trade profile: {}'.format(company['name']),
    }


def test_company_profile_list_with_params_redirects_to_search(client):
    url = reverse('public-company-profiles-list')
    response = client.get(url, {'sectors': 'AEROSPACE'})

    assert response.status_code == 302
    assert response.get('Location') == '/trade/search/?sector=AEROSPACE'


def test_company_profile_list_redirects_to_search(client):
    url = reverse('public-company-profiles-list')
    response = client.get(url)

    assert response.status_code == 302
    assert response.get('Location') == '/trade/search/'


@patch.object(helpers, 'get_company_profile')
def test_public_profile_details_calls_api(
    mock_retrieve_profile, client, retrieve_profile_data
):
    mock_retrieve_profile.return_value = retrieve_profile_data
    url = reverse(
        'public-company-profiles-detail',
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
        'public-company-profiles-detail',
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
        'public-company-profiles-detail',
        kwargs={'company_number': '01234567', 'slug': 'thing'}
    )

    response = client.get(url)

    assert response.status_code == http.client.NOT_FOUND


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
    assert mock_retrieve_public_case_study.call_args == call(
        case_study_id='2'
    )


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

    assert response.status_code == http.client.MOVED_PERMANENTLY
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

    assert response.status_code == http.client.MOVED_PERMANENTLY
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
        'contact-company',
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
        'contact-company',
        kwargs={
            'company_number': retrieve_profile_data['number'],
        },
    )
    response = client.post(url, valid_contact_company_data)

    assert response.status_code == 302
    assert response.url == reverse(
        'contact-company-sent',
        kwargs={'company_number': retrieve_profile_data['number']}
    )
    assert mock_save.call_count == 1
    assert mock_save.call_args == call(
        recipients=['test@example.com'],
        subject=settings.CONTACT_SUPPLIER_SUBJECT,
        reply_to=[valid_contact_company_data['email_address']],
        sender={
            'email_address': 'jim@example.com', 'country_code': 'China'
        },
        spam_control={'contents': ['greetings', 'and salutations']},
        recipient_name='Great company',
        form_url=url,
    )


@patch.object(views.ContactCompanyView.form_class.action_class, 'save')
def test_contact_company_view_feature_submit_api_forms_failure(
    mock_save, api_response_400, client,
    valid_contact_company_data, retrieve_profile_data,
):
    mock_save.return_value = api_response_400
    url = reverse(
        'contact-company',
        kwargs={
            'company_number': retrieve_profile_data['number'],
        },
    )
    with pytest.raises(requests.exceptions.HTTPError):
        client.post(url, valid_contact_company_data)


@patch.object(views.api_client.company, 'retrieve_public_profile', Mock)
@patch.object(helpers, 'get_public_company_profile_from_response')
def test_contact_company_exposes_context(
    mock_get_public_company_profile_from_response, client
):
    mock_get_public_company_profile_from_response.return_value = expected = {
        'number': '01234567',
        'slug': 'thing',
    }
    url = reverse(
        'contact-company',
        kwargs={'company_number': '01234567'}
    )

    response = client.get(url)
    assert response.status_code == http.client.OK
    assert response.template_name == [views.ContactCompanyView.template_name]
    assert response.context_data['company'] == expected


@patch('company.views.CompanySearchView.get_results_and_count')
def test_company_search_submit_form_on_get(
    mock_get_results_and_count, client, search_results
):
    results = [{'number': '1234567', 'slug': 'thing'}]
    mock_get_results_and_count.return_value = (results, 20)

    response = client.get(reverse('company-search'), {'term': '123'})

    assert response.status_code == 200
    assert response.context_data['results'] == results


@patch('company.views.CompanySearchView.get_results_and_count')
def test_company_search_pagination_count(
    mock_get_results_and_count, client, search_results
):
    results = [{'number': '1234567', 'slug': 'thing'}]
    mock_get_results_and_count.return_value = (results, 20)

    response = client.get(reverse('company-search'), {'term': '123'})

    assert response.status_code == 200
    assert response.context_data['pagination'].paginator.count == 20


@patch('directory_api_client.client.api_client.company.search_company')
def test_company_search_pagination_param(
    mock_search, client, search_results, api_response_search_200
):
    mock_search.return_value = api_response_search_200

    url = reverse('company-search')
    response = client.get(
        url, {'term': '123', 'page': 1, 'sectors': ['AEROSPACE']}
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

    url = reverse('company-search')
    response = client.get(
        url, {'term': '123', 'page': 1, 'sectors': ''}
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

    url = reverse('company-search')
    response = client.get(url, {'term': '123', 'page': 100})

    assert response.status_code == 302
    assert response.get('Location') == '/trade/search/?term=123'


@patch('company.views.CompanySearchView.get_results_and_count')
def test_company_search_not_submit_without_params(
    mock_get_results_and_count, client
):
    response = client.get(reverse('company-search'))

    assert response.status_code == 200
    mock_get_results_and_count.assert_not_called()


def test_company_search_sets_active_view_name(client):
    expected_value = 'public-company-profiles-list'

    response = client.get(reverse('company-search'))

    assert response.status_code == 200
    assert response.context_data['active_view_name'] == expected_value


@patch('directory_api_client.client.api_client.company.search_company')
def test_company_search_api_call_error(mock_search, api_response_400, client):
    mock_search.return_value = api_response_400

    with pytest.raises(requests.exceptions.HTTPError):
        client.get(reverse('company-search'), {'term': '123'})


@patch('directory_api_client.client.api_client.company.search_company')
@patch('company.helpers.get_results_from_search_response')
def test_company_search_api_success(
    mock_get_results_from_search_response, mock_search,
    api_response_search_200, client
):
    mock_search.return_value = api_response_search_200
    mock_get_results_from_search_response.return_value = {
        'results': [],
        'hits': {'total': 2}
    }
    response = client.get(reverse('company-search'), {'term': '123'})

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

    response = client.get(reverse('company-search'), {'term': 'wolf'})

    assert b'this is a short summary' in response.content


@patch('directory_api_client.client.api_client.company.search_company')
def test_company_highlight_description(
    mock_search, api_response_search_description_highlight_200, client
):
    mock_search.return_value = api_response_search_description_highlight_200

    response = client.get(reverse('company-search'), {'term': 'wolf'})
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

    response = client.get(reverse('company-search'), {'term': 'wolf'})

    assert b'<em>wolf</em> in sheep clothing summary.' in response.content


@pytest.mark.parametrize('name,number,slug', [
    ['public-company-profiles-detail',          '01234567',   'a'],
    ['public-company-profiles-detail',          'SC01234567', 'a'],
    ['public-company-profiles-detail-slugless', '01234567',   None],
    ['public-company-profiles-detail-slugless', 'SC01234567', None],
    ['contact-company',                         '01234567',   None],
    ['contact-company',                         'SC01234567', None],
])
def test_company_profile_url_routing_200(name, number, slug):
    kwargs = {'company_number': number}
    if slug:
        kwargs['slug'] = slug

    assert reverse(name, kwargs=kwargs)


@pytest.mark.parametrize('name,number,slug', [
    ['public-company-profiles-detail',          '.', 'a'],
    ['public-company-profiles-detail-slugless', '.', None],
    ['contact-company',                         '.', 'a'],
])
def test_company_profile_url_routing_404(name, number, slug):
    kwargs = {'company_number': number}
    if slug:
        kwargs['slug'] = slug

    with pytest.raises(NoReverseMatch):
        assert reverse(name, kwargs=kwargs)


def test_contact_company_sent_no_referer(client):
    url = reverse(
        'contact-company-sent', kwargs={'company_number': '01111111'}
    )
    expected_url = reverse(
        'contact-company', kwargs={'company_number': '01111111'}
    )
    response = client.get(url, {})

    assert response.status_code == 302
    assert response.url == expected_url


def test_contact_company_sent_incorrect_referer(client):
    url = reverse(
        'contact-company-sent', kwargs={'company_number': '01111111'}
    )
    expected_url = reverse(
        'contact-company', kwargs={'company_number': '01111111'}
    )
    referer_url = 'http://www.googe.com'
    response = client.get(url, {}, HTTP_REFERER=referer_url)

    assert response.status_code == 302
    assert response.url == expected_url


def test_contact_company_sent_correct_referer(client):
    url = reverse(
        'contact-company-sent', kwargs={'company_number': '01111111'}
    )
    referer_url = reverse(
        'contact-company', kwargs={'company_number': '01111111'}
    )
    response = client.get(url, {}, HTTP_REFERER=referer_url)

    assert response.status_code == 200
    assert response.template_name == [
        views.ContactCompanySentView.template_name
    ]
