from unittest.mock import patch, PropertyMock
from bs4 import BeautifulSoup
from django.utils import translation

from django.core.urlresolvers import reverse

from core.tests.helpers import create_response


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


@patch('core.views.LandingPageCMSView.cms_component',
       new_callable=PropertyMock)
@patch('core.views.LandingPageCMSView.page', new_callable=PropertyMock)
def test_landing_page_cms_component(
    mock_get_page, mock_get_component, client, settings
):
    settings.FEATURE_FLAGS['EU_EXIT_BANNER_ON'] = True
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
    settings.FEATURE_FLAGS['EU_EXIT_BANNER_ON'] = True
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
    response = client.get('/trade/?lang=ar')
    soup = BeautifulSoup(response.content, 'html.parser')

    assert soup.select('.banner-container')[0].get('dir') == 'rtl'
