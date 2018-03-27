from unittest.mock import patch

from django.urls import reverse

from core.tests import helpers


@patch('core.helpers.cms_client.find_a_supplier.list_industry_pages')
@patch('core.helpers.cms_client.find_a_supplier.get_landing_page')
def test_landing_page_context(
    mock_get_landing_page, mock_list_industry_pages, settings, client
):
    settings.FEATURE_CMS_ENABLED = True

    mock_get_landing_page.return_value = helpers.create_response(
        status_code=200,
        json_payload={'title': 'the page', 'languages': ['en-gb']}
    )

    mock_list_industry_pages.return_value = helpers.create_response(
        status_code=200, json_payload={'items': [{'title': 'good 1'}]}
    )

    response = client.get(reverse('index'))

    assert response.status_code == 200
    assert response.context_data['page'] == {
        'title': 'the page',
        'languages': ['en-gb'],
    }
    assert response.context_data['pages'] == [{'title': 'good 1'}]


@patch('core.helpers.cms_client.find_a_supplier.list_industry_pages')
@patch('core.helpers.cms_client.find_a_supplier.get_landing_page')
def test_landing_page_not_found(
    mock_get_landing_page, mock_list_industry_pages, settings, client
):
    settings.FEATURE_CMS_ENABLED = True

    mock_get_landing_page.return_value = helpers.create_response(
        status_code=404
    )

    mock_list_industry_pages.return_value = helpers.create_response(
        status_code=200, json_payload={'items': [{'title': 'good 1'}]}
    )

    response = client.get(reverse('index'))

    assert response.status_code == 404
