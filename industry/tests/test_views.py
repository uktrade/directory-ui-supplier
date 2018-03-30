from unittest.mock import call, patch

import pytest

from django.core.urlresolvers import resolve, reverse

from core.tests.helpers import create_response


details_cms_urls = (
    reverse(
        'sector-detail-cms-verbose', kwargs={'slug': 'slug', 'cms_page_id': 1}
    ),
    reverse('sector-article', kwargs={'slug': 'slug', 'cms_page_id': 2}),
)
list_cms_urls = (
    reverse('sector-list'),
)
cms_urls = details_cms_urls + list_cms_urls


@pytest.fixture
def industry_detail_data():
    return {
        'sector_value': 'value',
        'meta': {
            'languages': ['en-gb'],
            'slug': 'slug',
            'url': 'https://www.example.com/1/slug/'
        }
    }


@pytest.fixture
def industry_list_data():
    return {
        'title': 'the page',
        'industries': [{'title': 'good 1'}],
        'meta': {
            'languages': ['en-gb'],
            'slug': 'slug',
        },
    }


@pytest.fixture
def industry_article_data():
    return {
        'title': 'Hello world',
        'body': '<h2>Hello world</h2>',
        'date': '2018-01-01',
        'meta': {
            'languages': ['en-gb'],
            'slug': 'slug',
            'url': 'https://www.example.com/1/slug/'
        }
    }


@pytest.fixture(autouse=True)
def mock_get_page(industry_detail_data, industry_article_data):
    def side_effect(page_id, *args, **kwargs):
        return {
            '1': create_response(json_payload=industry_detail_data),
            '2': create_response(json_payload=industry_article_data),
        }[page_id]

    stub = patch('core.helpers.cms_client.get_page', side_effect=side_effect)
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


@pytest.mark.parametrize('url', cms_urls)
def test_cms_pages_feature_flag_on(
    mock_get_showcase_companies, settings, client, url
):
    settings.FEATURE_CMS_ENABLED = True

    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.parametrize('url', details_cms_urls)
def test_cms_pages_feature_flag_off(settings, client, url):
    settings.FEATURE_CMS_ENABLED = False

    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.parametrize('url', details_cms_urls)
def test_cms_pages_cms_client_params(settings, client, url, mock_get_page):
    settings.FEATURE_CMS_ENABLED = True

    response = client.get(url, {'draft_token': '123', 'lang': 'de'})

    assert response.status_code == 200
    assert mock_get_page.call_count == 1
    assert mock_get_page.call_args == call(
        page_id=resolve(url).kwargs['cms_page_id'],
        draft_token='123',
        language_code='de',
    )


@pytest.mark.parametrize('url', (
    reverse(
        'sector-detail-cms-verbose',
        kwargs={'slug': 'a', 'cms_page_id': 1}
    ),
    reverse(
        'sector-article',
        kwargs={'slug': 'a', 'cms_page_id': 2}
    ),
))
def test_cms_pages_cms_slug(settings, client, url):
    settings.FEATURE_CMS_ENABLED = True

    response = client.get(url)

    assert response.status_code == 302


@pytest.mark.parametrize('url', details_cms_urls)
def test_cms_pages_cms_page_404(settings, client, url, mock_get_page):
    mock_get_page.side_effect = None
    mock_get_page.return_value = create_response(status_code=404)

    settings.FEATURE_CMS_ENABLED = True

    response = client.get(url)

    assert response.status_code == 404


def test_industry_page_context(
    mock_get_showcase_companies, settings, client, industry_detail_data
):
    settings.FEATURE_CMS_ENABLED = True

    url = reverse(
        'sector-detail-cms-verbose',
        kwargs={'cms_page_id': '1', 'slug': 'slug'}
    )
    response = client.get(url)

    assert mock_get_showcase_companies.call_count == 1
    assert mock_get_showcase_companies.call_args == call(
        sectors='value', size=6
    )
    assert response.context_data['page'] == industry_detail_data
    assert response.template_name == ['industry/detail.html']


def test_article_page_context(settings, client, industry_article_data):
    settings.FEATURE_CMS_ENABLED = True

    url = reverse(
        'sector-article',
        kwargs={'cms_page_id': '2', 'slug': 'slug'}
    )
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
