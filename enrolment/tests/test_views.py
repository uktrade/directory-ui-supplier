import http
import requests
from unittest.mock import patch, Mock

import pytest

from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView

from zenpy.lib.api_objects import Ticket, User

from enrolment import constants, forms
from enrolment.views import (
    api_client,
    AnonymousSubscribeFormView,
    LeadGenerationFormView,
    InternationalLandingSectorDetailView,
    ConditionalEnableTranslationsMixin,
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
    pages = InternationalLandingSectorDetailView.get_active_pages()
    for slug, values in pages.items():
        context = values['context']
        template_name = values['template']
        url = reverse('international-sector-detail', kwargs={'slug': slug})

        response = client.get(url)

        assert response.status_code == http.client.OK
        assert response.template_name == [template_name]
        assert response.context_data['case_study'] == context['case_study']
        assert response.context_data['companies'] == context['companies']


def test_international_landing_page_sector_context(client):
    pages = InternationalLandingSectorDetailView.get_active_pages()
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


@pytest.mark.django_db
@patch.object(api_client.buyer, 'send_form')
def test_subscribe_view_submit(
    mock_send_form, buyer_request, buyer_form_data
):
    response = AnonymousSubscribeFormView.as_view()(buyer_request)
    expected_template = AnonymousSubscribeFormView.success_template

    assert response.status_code == http.client.OK
    assert response.template_name == expected_template
    mock_send_form.assert_called_once_with(
        forms.serialize_anonymous_subscriber_forms(buyer_form_data)
    )


@pytest.mark.django_db
@patch('zenpy.lib.api.UserApi.create_or_update')
@patch('zenpy.lib.api.TicketApi.create')
def test_lead_generation_view_submit_with_comment(
    mock_ticket_create, mock_user_create_or_update, buyer_request,
    buyer_form_data
):
    mock_user_create_or_update.return_value = Mock(id=999)
    response = LeadGenerationFormView.as_view()(buyer_request)

    assert response.status_code == http.client.OK
    assert response.template_name == LeadGenerationFormView.success_template

    assert mock_user_create_or_update.call_count == 1
    user = mock_user_create_or_update.call_args[0][0]
    assert user.__class__ == User
    assert user.email == buyer_form_data['email_address']
    assert user.name == buyer_form_data['full_name']

    assert mock_ticket_create.call_count == 1
    ticket = mock_ticket_create.call_args[0][0]
    assert ticket.__class__ == Ticket
    assert ticket.subject == 'Trade Profiles feedback'
    assert ticket.submitter_id == 999
    assert ticket.requester_id == 999
    description = (
        'Name: {full_name}\n'
        'Email: {email_address}\n'
        'Company: {company_name}\n'
        'Country: {country}\n'
        'Comment: {comment}'
    ).format(**buyer_form_data)
    assert ticket.description == description


@pytest.mark.django_db
@patch('zenpy.lib.api.UserApi.create_or_update')
@patch('zenpy.lib.api.TicketApi.create')
@patch.object(api_client.buyer, 'send_form')
def test_subscribe_view_submit_invalid(
    mock_send_form, mock_ticket_create, mock_user_create_or_update,
    buyer_request_invalid
):
    response = AnonymousSubscribeFormView.as_view()(buyer_request_invalid)

    assert response.template_name == [AnonymousSubscribeFormView.template_name]
    assert response.status_code == http.client.OK
    assert response.context_data['form'].errors
    assert mock_send_form.called is False
    assert mock_user_create_or_update.called is False
    assert mock_ticket_create.called is False


def test_international_landing_page_flag_on_advanced_manufacturing(settings):
    settings.FEATURE_ADVANCED_MANUFACTURING_ENABLED = True
    view = InternationalLandingSectorDetailView

    assert 'advanced-manufacturing' in view.get_active_pages()


def test_international_landing_page_flag_off_advanced_manufacturing(settings):
    settings.FEATURE_ADVANCED_MANUFACTURING_ENABLED = False
    view = InternationalLandingSectorDetailView

    assert 'advanced-manufacturing' not in view.get_active_pages()


def test_industry_list_page_flag_on_translations(settings, client):
    settings.FEATURE_INDUSTRIES_TRANSLATIONS_ENABLED = True

    url = reverse('international-sector-list')

    response = client.get(url)

    assert response.status_code == http.client.OK
    assert 'language_switcher' in response.context_data


def test_industry_list_page_flag_off_translations(settings, client):
    settings.FEATURE_INDUSTRIES_TRANSLATIONS_ENABLED = False

    url = reverse('international-sector-list')

    response = client.get(url)

    assert response.status_code == http.client.OK
    assert 'language_switcher' not in response.context_data


def test_industry_page_flag_on_translations(settings, client):
    settings.FEATURE_INDUSTRIES_TRANSLATIONS_ENABLED = True

    url = reverse('international-sector-detail', kwargs={'slug': 'health'})

    response = client.get(url)

    assert response.status_code == http.client.OK
    assert 'language_switcher' in response.context_data


def test_industry_page_flag_off_translations(client):
    settings.FEATURE_INDUSTRIES_TRANSLATIONS_ENABLED = False

    url = reverse('international-sector-detail', kwargs={'slug': 'health'})

    response = client.get(url)

    assert response.status_code == http.client.OK
    assert 'language_switcher' not in response.context_data


def test_international_landing_view_translations(client):
    url = reverse('index')

    response = client.get(url)

    assert response.status_code == http.client.OK
    assert 'language_switcher' in response.context_data


def test_conditional_translate_bidi_template(rf):
    class View(ConditionalEnableTranslationsMixin, TemplateView):
        template_name_bidi = 'bidi.html'
        template_name = 'non-bidi.html'

    view = View.as_view()
    request = rf.get('/')
    request.LANGUAGE_CODE = 'ar'

    response = view(request)

    assert response.status_code == 200
    assert response.template_name == ['bidi.html']


def test_conditional_translate_non_bidi_template(rf):
    class View(ConditionalEnableTranslationsMixin, TemplateView):
        template_name_bidi = 'bidi.html'
        template_name = 'non-bidi.html'

    view = View.as_view()
    request = rf.get('/')
    request.LANGUAGE_CODE = 'en-gb'

    response = view(request)

    assert response.status_code == 200
    assert response.template_name == ['non-bidi.html']
