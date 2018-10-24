import pytest


@pytest.mark.parametrize('source_url,destination_url', (
    ('/industries/creative/', '/industries/creative-services/'),
    ('/industries/health/', '/industries/healthcare/'),
    ('/industries/tech/', '/industries/technology/'),
    ('/industries/legal/', '/industries/legal-services/'),
))
def test_redirects(source_url, destination_url, client):
    response = client.get(source_url)

    assert response.status_code == 302
    assert response.url == destination_url
