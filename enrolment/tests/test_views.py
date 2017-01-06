import http
import requests
from unittest.mock import patch

import pytest

from django.core.urlresolvers import reverse

from enrolment import constants, forms
from enrolment.views import (
    api_client,
    InternationalLandingView,
    InternationalLandingSectorListView,
    InternationalLandingSectorDetailView
)


@pytest.fixture
def buyer_form_data():
    return {
        'full_name': 'Jim Example',
        'email_address': 'jim@example.com',
        'sector': 'AEROSPACE',
        'terms': True
    }


@pytest.fixture
def buyer_request(rf, client, buyer_form_data):
    request = rf.post('/', buyer_form_data)
    request.session = client.session
    return request


@pytest.fixture
def anon_request(rf, client):
    request = rf.get('/')
    request.session = client.session
    return request


@pytest.fixture
def api_response_200(*args, **kwargs):
    response = requests.Response()
    response.status_code = http.client.OK
    return response


@pytest.fixture
def api_response_400(*args, **kwargs):
    response = requests.Response()
    response.status_code = http.client.BAD_REQUEST
    return response


@pytest.fixture
def api_response_company_profile_no_sectors_200(api_response_200):
    response = api_response_200
    payload = {
        'website': 'http://example.com',
        'description': 'Ecommerce website',
        'number': 123456,
        'sectors': None,
        'logo': 'nice.jpg',
        'name': 'Great company',
        'keywords': 'word1 word2',
        'employees': '501-1000',
        'date_of_creation': '2015-03-02',
    }
    response.json = lambda: payload
    return response


@pytest.fixture
def api_response_company_profile_no_date_of_creation_200(api_response_200):
    response = api_response_200
    payload = {
        'website': 'http://example.com',
        'description': 'Ecommerce website',
        'number': 123456,
        'sectors': None,
        'logo': 'nice.jpg',
        'name': 'Great company',
        'keywords': 'word1 word2',
        'employees': '501-1000',
        'date_of_creation': None,
    }
    response.json = lambda: payload
    return response


@patch.object(api_client.buyer, 'send_form')
def test_international_landing_view_submit(
    mock_send_form, buyer_request, buyer_form_data
):
    response = InternationalLandingView.as_view()(buyer_request)

    assert response.template_name == InternationalLandingView.success_template
    mock_send_form.assert_called_once_with(
        forms.serialize_international_buyer_forms(buyer_form_data)
    )


@patch.object(api_client.buyer, 'send_form')
def test_international_landing_sector_list_view_submit(
    mock_send_form, buyer_request, buyer_form_data
):
    response = InternationalLandingSectorListView.as_view()(buyer_request)
    expected_template = InternationalLandingSectorListView.success_template

    assert response.template_name == expected_template
    mock_send_form.assert_called_once_with(
        forms.serialize_international_buyer_forms(buyer_form_data)
    )


def test_international_landing_page_sector_specific_unknown(client):
    url = reverse('international-sector-detail', kwargs={'slug': 'jam'})

    response = client.get(url)

    assert response.status_code == http.client.NOT_FOUND


def test_international_landing_page_sector_specific_known(client):
    for slug, values in InternationalLandingSectorDetailView.pages.items():
        context = values['context']
        template_name = values['template']
        url = reverse('international-sector-detail', kwargs={'slug': slug})

        response = client.get(url)

        assert response.status_code == http.client.OK
        assert response.template_name == [template_name]
        assert response.context_data['case_study'] == context['case_study']
        assert response.context_data['companies'] == context['companies']


def test_international_landing_page_sector_context(client):
    pages = InternationalLandingSectorDetailView.pages
    assert pages['health']['context'] == constants.HEALTH_SECTOR_CONTEXT
    assert pages['tech']['context'] == constants.TECH_SECTOR_CONTEXT
    assert pages['creative']['context'] == constants.CREATIVE_SECTOR_CONTEXT
    assert pages['food-and-drink']['context'] == constants.FOOD_SECTOR_CONTEXT


def test_terms_page_success(client):
    url = reverse('terms-and-conditions')

    response = client.get(url)

    assert response.status_code == http.client.OK


def test_privacy_cookiues_success(client):
    url = reverse('privacy-and-cookies')

    response = client.get(url)

    assert response.status_code == http.client.OK
