from unittest.mock import call, patch, Mock, PropertyMock
from bs4 import BeautifulSoup
from django.utils import translation

from django.core.urlresolvers import reverse

from core.tests.helpers import create_response
from core import views


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@patch('core.views.LandingPageCMSView.page', new_callable=PropertyMock)
def test_landing_page_context(
    mock_get_landing_page, mock_get_component, settings, client, breadcrumbs
):
    page = {
        'title': 'the page',
        'industries': [{'title': 'good 1'}],
        'meta': {'languages': ['en-gb']},
        'breadcrumbs': breadcrumbs,
    }
    mock_get_landing_page.return_value = page
    mock_get_component.return_value = create_response(
        status_code=200,
        json_payload={
            'banner_label': 'EU Exit updates',
            'banner_content': '<p>Lorem ipsum.</p>',
            'meta': {'languages': [('ar', 'العربيّة')]},
        }
    )

    response = client.get(reverse('index'))

    assert response.status_code == 200
    assert response.context_data['page'] == page


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_landing_page_not_found(
    mock_get_landing_page, settings, client
):
    mock_get_landing_page.return_value = create_response(
        status_code=404
    )

    response = client.get(reverse('index'))

    assert response.status_code == 404


@patch('zenpy.lib.api.UserApi.create_or_update')
@patch('zenpy.lib.api.TicketApi.create')
def test_lead_generation_submit_with_comment(
    mock_ticket_create, mock_user_create_or_update, client, captcha_stub,
    settings
):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'DIRECTORY_FORMS_API_ON': False,
    }
    mock_user_create_or_update.return_value = Mock(id=999)
    url = reverse('lead-generation')
    data = {
        'full_name': 'Jeff',
        'email_address': 'jeff@example.com',
        'company_name': 'My name is Jeff',
        'country': 'United Kingdom',
        'comment': 'hello',
        'terms': True,
        'g-recaptcha-response': captcha_stub,
    }
    response = client.post(url, data)

    assert response.status_code == 200
    assert (
        response.template_name == views.LeadGenerationFormView.success_template
    )

    assert mock_user_create_or_update.call_count == 1
    user = mock_user_create_or_update.call_args[0][0]
    assert user.email == data['email_address']
    assert user.name == data['full_name']

    assert mock_ticket_create.call_count == 1
    ticket = mock_ticket_create.call_args[0][0]
    assert ticket.subject == settings.ZENDESK_TICKET_SUBJECT
    assert ticket.submitter_id == 999
    assert ticket.requester_id == 999

    assert ticket.description == (
        'Name: Jeff\n'
        'Email: jeff@example.com\n'
        'Company: My name is Jeff\n'
        'Country: United Kingdom\n'
        'Comment: hello'
    )


@patch('zenpy.lib.api.UserApi.create_or_update')
@patch('zenpy.lib.api.TicketApi.create')
def test_contact_form_submit_with_comment_no_captcha(
    mock_ticket_create, mock_user_create_or_update, client, settings
):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'DIRECTORY_FORMS_API_ON': False,
    }
    mock_user_create_or_update.return_value = Mock(id=999)
    url = reverse('lead-generation')
    data = {
        'full_name': 'Jeff',
        'email_address': 'jeff@example.com',
        'company_name': 'My name is Jeff',
        'country': 'United Kingdom',
        'comment': 'hello',
        'terms': True,
    }
    response = client.post(url, data)

    assert 'This field is required' in str(response.content)


@patch.object(views.LeadGenerationFormView.form_class.action_class, 'save')
def test_contact_form_submit_with_comment_forms_api(
    mock_save, client, captcha_stub, settings
):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'DIRECTORY_FORMS_API_ON': True,
    }
    mock_save.return_value = create_response(status_code=200)

    url = reverse('lead-generation')
    data = {
        'full_name': 'Jeff',
        'email_address': 'jeff@example.com',
        'company_name': 'My name is Jeff',
        'country': 'United Kingdom',
        'comment': 'hello',
        'terms': True,
        'g-recaptcha-response': captcha_stub,
    }
    response = client.post(url, data)

    assert response.status_code == 200
    assert (
        response.template_name == views.LeadGenerationFormView.success_template
    )
    assert mock_save.call_count == 1
    assert mock_save.call_args == call({
        'company_name': 'My name is Jeff',
        'email_address': 'jeff@example.com',
        'country': 'United Kingdom',
        'full_name': 'Jeff',
        'comment': 'hello',
    })


@patch('core.views.LandingPageCMSView.cms_component',
       new_callable=PropertyMock)
@patch('core.views.LandingPageCMSView.page', new_callable=PropertyMock)
def test_landing_page_cms_component(
    mock_get_page, mock_get_component, client, settings
):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'EU_EXIT_BANNER_ON': True,
    }
    mock_get_page.return_value = {
        'title': 'the page',
        'sectors': [],
        'guides': [],
        'meta': {'languages': [('en-gb', 'English')]},
    }
    mock_get_component.return_value = {
        'banner_label': 'EU Exit updates',
        'banner_content': '<p>Lorem ipsum.</p>',
        'meta': {'languages': [('en-gb', 'English')]},
    }

    url = reverse('index')
    response = client.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    assert soup.select('.banner-container')[0].get('dir') == 'ltr'
    assert response.template_name == ['core/landing-page.html']
    assert 'EU Exit updates' in str(response.content)
    assert '<p class="body-text">Lorem ipsum.</p>' in str(response.content)


@patch('core.views.LandingPageCMSView.cms_component',
       new_callable=PropertyMock)
@patch('core.views.LandingPageCMSView.page', new_callable=PropertyMock)
def test_landing_page_cms_component_bidi(
    mock_get_page, mock_get_component, client, settings
):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'EU_EXIT_BANNER_ON': True,
    }
    mock_get_page.return_value = {
        'title': 'the page',
        'sectors': [],
        'guides': [],
        'meta': {'languages': [('ar', 'العربيّة')]},
    }
    mock_get_component.return_value = {
        'banner_label': 'EU Exit updates',
        'banner_content': '<p>Lorem ipsum.</p>',
        'meta': {'languages': [('ar', 'العربيّة')]},
    }

    translation.activate('ar')
    response = client.get('/?lang=ar')
    soup = BeautifulSoup(response.content, 'html.parser')

    assert soup.select('.banner-container')[0].get('dir') == 'rtl'
