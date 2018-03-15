from unittest.mock import call, patch

import pytest

from django.core.urlresolvers import resolve, reverse

from core.tests.helpers import create_response


cms_urls = (
    reverse(
        'sector-detail-cms-verbose', kwargs={'slug': 'tech', 'cms_page_id': 1}
    ),
    reverse('sector-article', kwargs={'slug': 'tech', 'cms_page_id': 2}),
)


@pytest.fixture
def industry_detail_response():
    return create_response(
        status_code=200,
        json_payload={
            'sector_value': 'value',
        }
    )


@pytest.fixture
def industry_article_response():
    return create_response(
        status_code=200,
        json_payload={
            'title': 'Hello world',
            'body': '<h2>Hello world</h2>',
            'date': '2018-01-01',
        }
    )


@pytest.fixture(autouse=True)
def mock_get_page(industry_detail_response, industry_article_response):
    def side_effect(page_id, *args, **kwargs):
        return {
            '1': industry_detail_response,
            '2': industry_article_response,
        }[page_id]

    stub = patch('core.helpers.cms_client.get_page', side_effect=side_effect)
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


@pytest.mark.parametrize('url', cms_urls)
def test_cms_pages_feature_flag_off(settings, client, url):
    settings.FEATURE_CMS_ENABLED = False

    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.parametrize('url', cms_urls)
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


@pytest.mark.parametrize('url', cms_urls)
def test_cms_pages_cms_page_404(settings, client, url, mock_get_page):
    mock_get_page.side_effect = None
    mock_get_page.return_value = create_response(status_code=404)

    settings.FEATURE_CMS_ENABLED = True

    response = client.get(url)

    assert response.status_code == 404


def test_industry_page_context(
    mock_get_showcase_companies, settings, client, industry_detail_response
):
    settings.FEATURE_CMS_ENABLED = True

    url = reverse(
        'sector-detail-cms-verbose',
        kwargs={'cms_page_id': '1', 'slug': 'thing'}
    )
    response = client.get(url)

    assert mock_get_showcase_companies.call_count == 1
    assert mock_get_showcase_companies.call_args == call(
        sectors='value', size=6
    )
    assert response.context_data['page'] == industry_detail_response.json()
    assert response.template_name == ['industry/sector-detail.html']


def test_article_page_context(settings, client, industry_article_response):
    settings.FEATURE_CMS_ENABLED = True

    url = reverse(
        'sector-article', kwargs={'cms_page_id': '2', 'slug': 'thing'}
    )
    response = client.get(url)

    assert response.context_data['page'] == industry_article_response.json()
    assert response.template_name == ['industry/sector-article.html']
