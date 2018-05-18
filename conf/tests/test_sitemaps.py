import http
from unittest.mock import patch

from django.core.urlresolvers import reverse

from core.tests.helpers import create_response


@patch('core.helpers.cms_client.list_by_page_type')
def test_sitemaps_200(mock_list_by_page_type, client):
    mock_list_by_page_type.return_value = create_response(
        json_payload={'items': []}
    )
    url = reverse('sitemap')

    response = client.get(url)

    assert response.status_code == http.client.OK
