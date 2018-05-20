from unittest.mock import patch

from django.core.urlresolvers import reverse

from core.tests import helpers


@patch('core.helpers.cms_client.lookup_by_slug')
def test_landing_page_context(
    mock_get_landing_page, settings, client, breadcrumbs
):
    page = {
        'title': 'the page',
        'industries': [{'title': 'good 1'}],
        'meta': {'languages': ['en-gb']},
        'breadcrumbs': breadcrumbs,
    }
    mock_get_landing_page.return_value = helpers.create_response(
        status_code=200,
        json_payload=page
    )

    response = client.get(reverse('index'))

    assert response.status_code == 200
    assert response.context_data['page'] == page


@patch('core.helpers.cms_client.lookup_by_slug')
def test_landing_page_not_found(
    mock_get_landing_page, settings, client
):
    mock_get_landing_page.return_value = helpers.create_response(
        status_code=404
    )

    response = client.get(reverse('index'))

    assert response.status_code == 404
