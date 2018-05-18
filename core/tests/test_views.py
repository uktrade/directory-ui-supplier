from unittest.mock import patch

import pytest

from django.core.urlresolvers import reverse

from core.tests import helpers


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
def buyer_request_invalid(rf, client):
    request = rf.post('/', {})
    request.session = client.session
    return request


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
