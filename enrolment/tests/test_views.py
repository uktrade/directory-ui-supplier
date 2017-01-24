import http
import requests
from unittest.mock import patch

import pytest

from django.conf import settings
from django.core.urlresolvers import reverse

from zenpy.lib.api_objects import Ticket

from enrolment import constants, forms
from enrolment.views import (
    api_client,
    BuyerSubscribeFormView,
    InternationalLandingSectorDetailView
)


@pytest.fixture
def buyer_form_data_no_comment():
    return {
        'full_name': 'Jim Example',
        'email_address': 'jim@example.com',
        'sector': 'AEROSPACE',
        'company_name': 'Deutsche Bank',
        'country': 'Germany',
        'terms': True,
    }


@pytest.fixture
def buyer_form_data():
    return {
        'full_name': 'Jim Example',
        'email_address': 'jim@example.com',
        'sector': 'AEROSPACE',
        'company_name': 'Deutsche Bank',
        'country': 'Germany',
        'terms': True,
        'comment': 'This website should be all in German.',
    }


@pytest.fixture
def buyer_request(rf, client, buyer_form_data):
    request = rf.post('/', buyer_form_data)
    request.session = client.session
    return request


@pytest.fixture
def buyer_request_no_comment(rf, client, buyer_form_data_no_comment):
    request = rf.post('/', buyer_form_data_no_comment)
    request.session = client.session
    return request


@pytest.fixture
def buyer_request_invalid(rf, client):
    request = rf.post('/', {})
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


def test_international_landing_view_context(client):
    response = client.get(reverse('index'))

    lang_context = response.context['language_switcher']

    assert lang_context['show']
    assert lang_context['form'].initial == {'lang': settings.LANGUAGE_CODE}
    assert response.context['active_view_name'] == 'index'


def test_international_landing_page_sector_context_verbose(client):
    url = reverse('international-sector-detail', kwargs={'slug': 'health'})

    response = client.get(url + '?verbose=true')

    assert response.status_code == http.client.OK
    assert response.context_data['show_proposition'] is True


def test_international_landing_page_sector_context_non_verbose(client):
    url = reverse('international-sector-detail', kwargs={'slug': 'health'})

    response = client.get(url)

    assert response.status_code == http.client.OK
    assert response.context_data['show_proposition'] is False


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


def test_international_sector_list_context(client):
    view_name = 'international-sector-list'
    response = client.get(reverse(view_name))

    assert response.context['active_view_name'] == view_name


def test_terms_page_success(client):
    url = reverse('terms-and-conditions')

    response = client.get(url)

    assert response.status_code == http.client.OK


def test_privacy_cookiues_success(client):
    url = reverse('privacy-and-cookies')

    response = client.get(url)

    assert response.status_code == http.client.OK


@patch('zenpy.lib.api.TicketApi.create')
@patch.object(api_client.buyer, 'send_form')
def test_subscribe_view_submit_with_comment(
    mock_send_form, mock_ticket_create, buyer_request, buyer_form_data,
    settings
):
    settings.ZENDESK_TICKET_SUBJECT = 'Be Zen!'
    response = BuyerSubscribeFormView.as_view()(buyer_request)

    assert response.status_code == http.client.OK
    assert response.template_name == BuyerSubscribeFormView.success_template
    mock_send_form.assert_called_once_with(
        forms.serialize_international_buyer_forms(buyer_form_data)
    )
    ticket = mock_ticket_create.call_args[0][0]
    assert ticket.__class__ == Ticket
    assert ticket.subject == 'Be Zen!'
    description = (
        'Name: {name}\n'
        'Email: {email}\n'
        'Company: {company}\n'
        'Country: {country}\n'
        'Sector: {sector}\n'
        'Comment: {comment}'
    ).format(
        name=buyer_form_data['full_name'],
        email=buyer_form_data['email_address'],
        company=buyer_form_data['company_name'],
        country=buyer_form_data['country'],
        sector=buyer_form_data['sector'],
        comment=buyer_form_data['comment'],
    )
    assert ticket.description == description


@patch('zenpy.lib.api.TicketApi.create')
@patch.object(api_client.buyer, 'send_form')
def test_subscribe_view_submit_without_comment(
    mock_send_form, mock_ticket_create, buyer_request_no_comment,
    buyer_form_data_no_comment
):
    response = BuyerSubscribeFormView.as_view()(buyer_request_no_comment)

    assert response.status_code == http.client.OK
    assert response.template_name == BuyerSubscribeFormView.success_template
    mock_send_form.assert_called_once_with(
        forms.serialize_international_buyer_forms(buyer_form_data_no_comment)
    )
    assert mock_ticket_create.called is False


@patch('zenpy.lib.api.TicketApi.create')
@patch.object(api_client.buyer, 'send_form')
def test_subscribe_view_submit_invalid(
    mock_send_form, mock_ticket_create, buyer_request_invalid
):
    response = BuyerSubscribeFormView.as_view()(buyer_request_invalid)

    assert response.template_name == [BuyerSubscribeFormView.template_name]
    assert response.status_code == http.client.OK
    assert response.context_data['form'].errors
    assert mock_send_form.called is False
    assert mock_ticket_create.called is False
