import pytest

from directory_constants.urls import FEEDBACK


@pytest.mark.parametrize('source_url,destination_url', (
    ('/trade/industries/creative/', '/trade/industries/creative-services/'),
    ('/trade/industries/health/', '/trade/industries/healthcare/'),
    ('/trade/industries/tech/', '/trade/industries/technology/'),
    ('/trade/industries/legal/', '/trade/industries/legal-services/'),
    ('/trade/feedback/', FEEDBACK),
))
def test_redirects(source_url, destination_url, client):
    response = client.get(source_url)

    assert response.status_code == 302
    assert response.url == destination_url
