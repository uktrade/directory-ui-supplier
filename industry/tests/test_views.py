from unittest.mock import call, patch, Mock

import pytest

from django.core.urlresolvers import resolve, reverse

from core.tests.helpers import create_response
from industry import constants, views


details_cms_urls = (
    reverse('sector-detail-verbose', kwargs={'slug': 'industry'}),
    reverse('sector-article', kwargs={'slug': 'article'}),
)
list_cms_urls = (
    reverse('sector-list'),
)
cms_urls = details_cms_urls + list_cms_urls


@pytest.fixture
def contact_page_data(breadcrumbs):
    return {
        'breadcrumbs': breadcrumbs,
        'meta': {
            'languages': ['en-gb'],
            'slug': 'contact-us',
            'url': 'https://www.example.com/industries/contact-us/',
            'pk': 'industry',
        }
    }


@pytest.fixture
def industry_detail_data(breadcrumbs):
    return {
        'search_filter_sector': ['value'],
        'search_filter_text': 'great',
        'search_filter_showcase_only': False,
        'breadcrumbs': breadcrumbs,
        'meta': {
            'languages': ['en-gb'],
            'slug': 'industry',
            'url': 'https://www.example.com/1/slug/',
            'pk': 'industry',
        }
    }


@pytest.fixture
def industry_list_data(breadcrumbs):
    return {
        'title': 'the page',
        'industries': [{'title': 'good 1'}],
        'breadcrumbs': breadcrumbs,
        'meta': {
            'languages': ['en-gb'],
            'slug': 'industry',
            'pk': 'article',
        },
    }


@pytest.fixture
def industry_article_data(breadcrumbs):
    return {
        'title': 'Hello world',
        'body': '<h2>Hello world</h2>',
        'date': '2018-01-01',
        'breadcrumbs': breadcrumbs,
        'meta': {
            'languages': ['en-gb'],
            'slug': 'article',
            'url': 'https://www.example.com/1/slug/',
            'pk': '3',
        }
    }


@pytest.fixture(autouse=True)
def mock_lookup_by_slug(industry_detail_data, industry_article_data):
    def side_effect(slug, *args, **kwargs):
        slug_1 = industry_detail_data['meta']['slug']
        slug_2 = industry_article_data['meta']['slug']
        return {
            slug_1: create_response(json_payload=industry_detail_data),
            slug_2: create_response(json_payload=industry_article_data),
        }[slug]

    stub = patch(
        'core.helpers.cms_client.lookup_by_slug', side_effect=side_effect
    )
    yield stub.start()
    stub.stop()


@pytest.fixture(autouse=True)
def mock_get_industries_list_page(industry_list_data):
    stub = patch(
        'core.helpers.cms_client.find_a_supplier.get_industries_landing_page',
        return_value=create_response(json_payload=industry_list_data)
    )
    yield stub.start()
    stub.stop()


@pytest.fixture(autouse=True)
def mock_get_showcase_companies():
    stub = patch('industry.views.get_showcase_companies', return_value=[])
    yield stub.start()
    stub.stop()


@pytest.fixture(autouse=True)
def mock_get_contact_page(contact_page_data):
    stub = patch(
        'core.helpers.cms_client.find_a_supplier.get_industry_contact_page',
        return_value=create_response(json_payload=contact_page_data)
    )
    yield stub.start()
    stub.stop()


@pytest.mark.parametrize('url', cms_urls)
def test_cms_pages_feature_flag_on(settings, client, url):
    settings.FEATURE_CMS_ENABLED = True

    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.parametrize('url', details_cms_urls)
def test_cms_pages_feature_flag_off(settings, client, url):
    settings.FEATURE_CMS_ENABLED = False

    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.parametrize('url', details_cms_urls)
def test_cms_pages_cms_client_params(
    settings, client, url, mock_lookup_by_slug
):
    settings.FEATURE_CMS_ENABLED = True

    response = client.get(url, {'draft_token': '123', 'lang': 'de'})

    assert response.status_code == 200
    assert mock_lookup_by_slug.call_count == 1
    assert mock_lookup_by_slug.call_args == call(
        slug=resolve(url).kwargs['slug'],
        draft_token='123',
        language_code='de',
    )


@pytest.mark.parametrize('url', (
    reverse('sector-detail-verbose', kwargs={'slug': 'industry'}),
    reverse('sector-article', kwargs={'slug': 'article'}),
))
def test_cms_pages_cms_slug(settings, client, url):
    settings.FEATURE_CMS_ENABLED = True

    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.parametrize('url', details_cms_urls)
def test_cms_pages_cms_page_404(settings, client, url, mock_lookup_by_slug):
    mock_lookup_by_slug.side_effect = None
    mock_lookup_by_slug.return_value = create_response(status_code=404)

    settings.FEATURE_CMS_ENABLED = True

    response = client.get(url)

    assert response.status_code == 404


def test_industry_page_context_curated_feature_enabled(
    mock_get_showcase_companies, settings, client, industry_detail_data
):
    settings.FEATURE_CMS_ENABLED = True
    industry_detail_data['search_filter_showcase_only'] = True

    url = reverse('sector-detail-verbose', kwargs={'slug': 'industry'})
    response = client.get(url)

    assert mock_get_showcase_companies.call_count == 1
    assert mock_get_showcase_companies.call_args == call(
        sectors=['value'], is_showcase_company=True, size=6, term='great'
    )
    assert response.context_data['page'] == industry_detail_data
    assert response.template_name == ['industry/detail.html']


def test_industry_page_context_curated_feature_disabled(
    mock_get_showcase_companies, settings, client, industry_detail_data
):
    settings.FEATURE_CMS_ENABLED = True
    industry_detail_data['search_filter_showcase_only'] = False

    url = reverse('sector-detail-verbose', kwargs={'slug': 'industry'})
    response = client.get(url)

    assert mock_get_showcase_companies.call_count == 1
    assert mock_get_showcase_companies.call_args == call(
        sectors=['value'], size=6, term='great'
    )
    assert response.context_data['page'] == industry_detail_data
    assert response.template_name == ['industry/detail.html']


def test_article_page_context(settings, client, industry_article_data):
    settings.FEATURE_CMS_ENABLED = True

    url = reverse('sector-article', kwargs={'slug': 'article'})
    response = client.get(url)

    assert response.context_data['page'] == industry_article_data
    assert response.template_name == ['industry/article.html']


@patch('core.helpers.cms_client.find_a_supplier.get_industries_landing_page')
def test_industries_page_context(
    mock_get_industries_landing_page, settings, client, industry_list_data
):
    settings.FEATURE_CMS_ENABLED = True
    mock_get_industries_landing_page.return_value = create_response(
        json_payload=industry_list_data,
    )

    response = client.get(reverse('sector-list'))

    assert response.status_code == 200
    assert response.context_data['page'] == industry_list_data


@patch('core.helpers.cms_client.find_a_supplier.get_industries_landing_page')
def test_industries_page_not_found(
    mock_get_industries_landing_page, settings, client
):
    settings.FEATURE_CMS_ENABLED = True
    mock_get_industries_landing_page.return_value = create_response(
        status_code=404
    )

    response = client.get(reverse('sector-list'))

    assert response.status_code == 404


@pytest.mark.django_db
@patch('zenpy.lib.api.UserApi.create_or_update')
@patch('zenpy.lib.api.TicketApi.create')
def test_contact_form_submit_with_comment(
    mock_ticket_create, mock_user_create_or_update, client
):
    mock_user_create_or_update.return_value = Mock(id=999)
    url = reverse('sector-detail-cms-contact', kwargs={'slug': 'industry'})
    data = {
        'full_name': 'Jeff',
        'email_address': 'jeff@example.com',
        'sector': 'AEROSPACE',
        'organisation_name': 'My name is Jeff',
        'organisation_size': '1-10',
        'country': 'United Kingdom',
        'body': 'hello',
        'source': constants.MARKETING_SOURCES[1][0],
        'terms_agreed': True,
    }
    response = client.post(url, data)

    assert response.status_code == 200
    assert response.template_name == (
        views.IndustryDetailContactCMSView.template_name_success
    )

    assert mock_user_create_or_update.call_count == 1
    user = mock_user_create_or_update.call_args[0][0]
    assert user.email == data['email_address']
    assert user.name == data['full_name']

    assert mock_ticket_create.call_count == 1
    ticket = mock_ticket_create.call_args[0][0]
    assert ticket.subject == 'AEROSPACE contact form submitted.'
    assert ticket.submitter_id == 999
    assert ticket.requester_id == 999

    assert ticket.description == (
        'Body: hello\n'
        'Country: United Kingdom\n'
        'Email Address: jeff@example.com\n'
        'Full Name: Jeff\n'
        'Organisation Name: My name is Jeff\n'
        'Organisation Size: 1-10\n'
        'Sector: AEROSPACE\n'
        'Source: Print - posters or billboards\n'
        'Source Other: \n'
        'Terms Agreed: True'
    )


@pytest.mark.django_db
def test_contact_form_prefills_sector(client, industry_detail_data):
    url = reverse('sector-detail-cms-contact', kwargs={'slug': 'industry'})
    response = client.get(url)

    assert response.context_data['form'].initial['sector'] == (
        industry_detail_data['search_filter_sector'][0]
    )


@pytest.mark.django_db
@patch('zenpy.lib.api.UserApi.create_or_update')
@patch('zenpy.lib.api.TicketApi.create')
@patch('core.helpers.cms_client.find_a_supplier.get_industries_landing_page')
def test_industry_list_contact_form_submit_with_comment(
    mock_get_industries_landing_page, mock_ticket_create,
    mock_user_create_or_update, client, industry_list_data, settings
):
    settings.FEATURE_CMS_ENABLED = True
    mock_get_industries_landing_page.return_value = create_response(
        json_payload=industry_list_data,
    )
    mock_user_create_or_update.return_value = Mock(id=999)
    url = reverse('sector-list-cms-contact')
    data = {
        'full_name': 'Jeff',
        'email_address': 'jeff@example.com',
        'sector': 'AEROSPACE',
        'organisation_name': 'My name is Jeff',
        'organisation_size': '1-10',
        'country': 'United Kingdom',
        'body': 'hello',
        'source': constants.MARKETING_SOURCES[1][0],
        'terms_agreed': True,
    }
    response = client.post(url, data)

    assert response.status_code == 200
    assert response.template_name == (
        views.IndustryDetailContactCMSView.template_name_success
    )

    assert mock_user_create_or_update.call_count == 1
    user = mock_user_create_or_update.call_args[0][0]
    assert user.email == data['email_address']
    assert user.name == data['full_name']

    assert mock_ticket_create.call_count == 1
    ticket = mock_ticket_create.call_args[0][0]
    assert ticket.subject == 'AEROSPACE contact form submitted.'
    assert ticket.submitter_id == 999
    assert ticket.requester_id == 999

    assert ticket.description == (
        'Body: hello\n'
        'Country: United Kingdom\n'
        'Email Address: jeff@example.com\n'
        'Full Name: Jeff\n'
        'Organisation Name: My name is Jeff\n'
        'Organisation Size: 1-10\n'
        'Sector: AEROSPACE\n'
        'Source: Print - posters or billboards\n'
        'Source Other: \n'
        'Terms Agreed: True'
    )
