from unittest.mock import call, patch, PropertyMock, Mock

from directory_cms_client.client import cms_api_client
import pytest

from django.core.urlresolvers import resolve, reverse

from core.tests.helpers import create_response
from industry import constants, views
from industry.views import IndustryDetailCMSView

details_cms_urls = (
    reverse('sector-article', kwargs={'slug': 'article'}),
)
list_cms_urls = (reverse('sector-list'),)
cms_urls = details_cms_urls + list_cms_urls


@pytest.fixture
def contact_page_data(breadcrumbs):
    return {
        'breadcrumbs': breadcrumbs,
        'industry_options': [
            {
                'breadcrumbs_label': 'Agriculture',
                'meta': {'slug': 'agriculture'},
            },
            {
                'breadcrumbs_label': 'Technology',
                'meta': {'slug': 'industry'},
            },
        ],
        'meta': {
            'languages': ['en-gb'],
            'slug': 'industry-contact',
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
        'breadcrumbs_label': 'Technology',
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
        'industries': [
            {'title': 'one', 'show_on_industries_showcase_page': False},
            {'title': 'two', 'show_on_industries_showcase_page': False},
            {'title': 'three', 'show_on_industries_showcase_page': True},
            {'title': 'four', 'show_on_industries_showcase_page': True}
        ],
        'breadcrumbs': breadcrumbs,
        'meta': {
            'languages': ['en-gb'],
            'slug': 'industries-landing-page',
            'pk': 'article',
        },
    }


@pytest.fixture
def industry_list_no_showcase_data(industry_list_data):
    data = industry_list_data
    data['industries'] = [
        {'title': i, 'show_on_industries_showcase_page': False}
        for i in range(19)
    ]
    return data


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
def mock_lookup_by_slug(
    industry_detail_data, industry_article_data, contact_page_data,
    industry_list_data, request
):
    def side_effect(slug, *args, **kwargs):
        if 'noautofixture' in request.keywords:
            return
        resources = [
            industry_detail_data,
            industry_article_data,
            contact_page_data,
            industry_list_data,
        ]
        return {
            resource['meta']['slug']: create_response(json_payload=resource)
            for resource in resources
        }[slug]

    stub = patch.object(
        cms_api_client, 'lookup_by_slug', side_effect=side_effect
    )
    yield stub.start()
    stub.stop()


@pytest.fixture(autouse=True)
def mock_get_showcase_companies():
    stub = patch('industry.views.get_showcase_companies', return_value=[])
    yield stub.start()
    stub.stop()


@pytest.mark.parametrize('url', cms_urls)
def test_cms_pages(settings, client, url):
    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.parametrize('url', details_cms_urls)
def test_cms_api_client_params(
    settings, client, url, mock_lookup_by_slug
):
    response = client.get(url, {'draft_token': '123', 'language': 'de'})

    assert response.status_code == 200
    assert mock_lookup_by_slug.call_count == 1
    assert mock_lookup_by_slug.call_args == call(
        slug=resolve(url).kwargs['slug'],
        draft_token='123',
        language_code='de',
    )


@pytest.mark.parametrize('url', (
    reverse('sector-article', kwargs={'slug': 'article'}),
))
def test_cms_pages_cms_slug(settings, client, url):

    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.parametrize('url', details_cms_urls)
def test_cms_pages_cms_page_404(settings, client, url, mock_lookup_by_slug):
    mock_lookup_by_slug.side_effect = None
    mock_lookup_by_slug.return_value = create_response(status_code=404)

    response = client.get(url)

    assert response.status_code == 404


@patch.object(IndustryDetailCMSView, 'international_industry_page',
              new_callable=PropertyMock)
def test_industry_page_context_curated_feature_enabled(
        mock_page_exists, mock_get_showcase_companies, client,
        industry_detail_data
):
    mock_page_exists.return_value = None
    industry_detail_data['search_filter_showcase_only'] = True

    url = reverse('sector-detail-verbose', kwargs={'slug': 'industry'})
    response = client.get(url)

    assert mock_get_showcase_companies.call_count == 1
    assert mock_get_showcase_companies.call_args == call(
        sectors=['value'], is_showcase_company=True, size=6, term='great'
    )
    assert response.context_data['page'] == industry_detail_data
    assert response.template_name == ['industry/detail.html']


@patch.object(IndustryDetailCMSView, 'international_industry_page',
              new_callable=PropertyMock)
def test_industry_page_context_curated_feature_disabled(
        mock_page_exists, mock_get_showcase_companies, settings, client,
        industry_detail_data
):
    mock_page_exists.return_value = None
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
    url = reverse('sector-article', kwargs={'slug': 'article'})
    response = client.get(url)

    assert response.context_data['page'] == industry_article_data
    assert response.template_name == ['industry/article.html']


@patch.object(cms_api_client, 'lookup_by_slug')
def test_industries_page_context(
    mock_get_industries_landing_page, settings, client, industry_list_data
):
    mock_get_industries_landing_page.return_value = create_response(
        json_payload=industry_list_data,
    )

    response = client.get(reverse('sector-list'))

    assert response.status_code == 200
    assert response.context_data['page'] == industry_list_data
    assert response.context_data['showcase_industries'] == [
        industry_list_data['industries'][2],
        industry_list_data['industries'][3],
    ]


@patch.object(cms_api_client, 'lookup_by_slug')
def test_industries_page_context_no_showcase_industries(
    mock_lookup_by_slug, settings, client, industry_list_no_showcase_data
):
    mock_lookup_by_slug.side_effect = None
    mock_lookup_by_slug.return_value = create_response(
        json_payload=industry_list_no_showcase_data,
    )

    response = client.get(reverse('sector-list'))

    assert response.status_code == 200
    assert response.context_data['page'] == industry_list_no_showcase_data
    assert response.context_data['showcase_industries'] == (
        industry_list_no_showcase_data['industries'][:9]
    )


@patch.object(cms_api_client, 'lookup_by_slug')
def test_industries_page_not_found(mock_lookup_by_slug, settings, client):
    mock_lookup_by_slug.return_value = create_response(status_code=404)

    response = client.get(reverse('sector-list'))

    assert response.status_code == 404


@patch.object(
    views.IndustryDetailContactCMSView.form_class.action_class, 'save'
)
def test_contact_form_submit_with_comment_forms_api(
    mock_save, client, captcha_stub
):
    mock_save.return_value = create_response(status_code=200)

    url = reverse('sector-detail-cms-contact', kwargs={'slug': 'industry'})
    data = {
        'full_name': 'Jeff',
        'email_address': 'jeff@example.com',
        'phone_number': '1231312',
        'sector': 'industry',
        'organisation_name': 'My name is Jeff',
        'organisation_size': '1-10',
        'country': 'United Kingdom',
        'body': 'hello',
        'source': constants.MARKETING_SOURCES[1][0],
        'terms_agreed': True,
        'g-recaptcha-response': captcha_stub,
    }
    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url == (
        reverse('sector-detail-cms-contact-sent', kwargs={'slug': 'industry'})
    )
    assert mock_save.call_count == 2
    assert mock_save.call_args_list[0] == mock_save.call_args_list[1] == call({
        'sector': 'industry',
        'organisation_name': 'My name is Jeff',
        'source_other': '',
        'organisation_size': '1-10',
        'email_address': 'jeff@example.com',
        'phone_number': '1231312',
        'country': 'United Kingdom',
        'full_name': 'Jeff',
        'body': 'hello',
        'source': constants.MARKETING_SOURCES[1][0],
    })


def test_contact_form_prefills_sector(client, industry_detail_data):
    url = reverse('sector-detail-cms-contact', kwargs={'slug': 'industry'})
    response = client.get(url)

    assert response.context_data['form'].initial['sector'] == (
        industry_detail_data['meta']['slug']
    )


@patch.object(views.IndustryLandingPageContactCMSView.form_class, 'save')
def test_sector_list_submit_with_comment_forms_api(
    mock_save, client, captcha_stub, settings
):
    mock_save.return_value = create_response(status_code=200)

    url = reverse('sector-list-cms-contact')
    data = {
        'full_name': 'Jeff',
        'email_address': 'jeff@example.com',
        'phone_number': '3223232',
        'sector': 'industry',
        'organisation_name': 'My name is Jeff',
        'organisation_size': '1-10',
        'country': 'United Kingdom',
        'body': 'hello',
        'source': constants.MARKETING_SOURCES[1][0],
        'terms_agreed': True,
        'g-recaptcha-response': captcha_stub,
    }
    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url == (
        reverse('sector-list-cms-contact-sent')
    )
    assert mock_save.call_count == 2
    assert mock_save.call_args_list[0] == call(
        email_address='buying@example.com',
        form_url='/trade/industries/contact/',
        sender={
            'email_address': 'jeff@example.com',
            'country_code': 'United Kingdom'
        },
        spam_control={
            'contents': ['hello']},
        template_id=settings.CONTACT_INDUSTRY_AGENT_TEMPLATE_ID,
    )
    assert mock_save.call_args_list[1] == call(
        email_address='jeff@example.com',
        form_url='/trade/industries/contact/',
        template_id=settings.CONTACT_INDUSTRY_USER_TEMPLATE_ID,
        email_reply_to_id=settings.CONTACT_INDUSTRY_USER_REPLY_TO_ID,
    )


def test_contact_industry_detail_sent_no_referer(client):
    url = reverse(
        'sector-detail-cms-contact-sent', kwargs={'slug': 'industry'}
    )
    expected_url = reverse(
        'sector-detail-cms-contact', kwargs={'slug': 'industry'}
    )
    response = client.get(url, {})

    assert response.status_code == 302
    assert response.url == expected_url


def test_contact_industry_detail_sent_incorrect_referer(client):
    url = reverse(
        'sector-detail-cms-contact-sent', kwargs={'slug': 'industry'}
    )
    expected_url = reverse(
        'sector-detail-cms-contact', kwargs={'slug': 'industry'}
    )
    referer_url = 'http://www.googe.com'
    response = client.get(url, {}, HTTP_REFERER=referer_url)

    assert response.status_code == 302
    assert response.url == expected_url


def test_contact_industry_detail_sent_correct_referer(client):
    url = reverse(
        'sector-detail-cms-contact-sent', kwargs={'slug': 'industry'}
    )
    referer_url = reverse(
        'sector-detail-cms-contact', kwargs={'slug': 'industry'}
    )
    response = client.get(url, {}, HTTP_REFERER=referer_url)

    assert response.status_code == 200
    assert response.template_name == [
        views.IndustryDetailContactCMSSentView.template_name
    ]


def test_contact_industry_list_sent_no_referer(client):
    url = reverse('sector-list-cms-contact-sent')
    expected_url = reverse('sector-list-cms-contact')
    response = client.get(url, {})

    assert response.status_code == 302
    assert response.url == expected_url


def test_contact_industry_list_sent_incorrect_referer(client):
    url = reverse('sector-list-cms-contact-sent')
    expected_url = reverse('sector-list-cms-contact')
    referer_url = 'http://www.googe.com'
    response = client.get(url, {}, HTTP_REFERER=referer_url)

    assert response.status_code == 302
    assert response.url == expected_url


def test_contact_industry_list_sent_correct_referer(client):
    url = reverse('sector-list-cms-contact-sent')
    referer_url = reverse('sector-list-cms-contact')
    response = client.get(url, {}, HTTP_REFERER=referer_url)

    assert response.status_code == 200
    assert response.template_name == [
        views.IndustryLandingPageContactCMSSentView.template_name
    ]


@pytest.mark.noautofixture
@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_industry_page_exists_in_international(mock_get_page, client):
    mocked_response = Mock(status_code=200)
    mocked_response.json.return_value = {'full_url': 'http://test.com'}
    mock_get_page.return_value = mocked_response
    url = reverse('sector-detail-verbose', kwargs={'slug': 'foo'})
    response = client.get(url)
    assert mock_get_page.call_args == call(draft_token=None,
                                           language_code='en-gb',
                                           service_name='GREAT_INTERNATIONAL',
                                           slug='foo')
    assert response.status_code == 302
    assert response.url == 'http://test.com'


@patch.object(IndustryDetailCMSView, 'international_industry_page',
              new_callable=PropertyMock)
def test_industry_page_does_not_exist_in_international(mock_page_exists,
                                                       client):
    mock_page_exists.return_value = None
    url = reverse('sector-detail-verbose', kwargs={'slug': 'industry'})
    response = client.get(url)
    assert response.status_code == 200
