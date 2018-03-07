import requests_mock

from core import helpers


def test_cms_secrets(settings):
    assert helpers.cms_client.base_url == settings.CMS_URL
    assert (
        helpers.cms_client.request_signer.secret ==
        settings.CMS_SIGNATURE_SECRET
    )


def test_cms_client_draft():
    client = helpers.DirectoryCMSClient(
        base_url='http://cms.com',
        api_key='debug',
    )
    with requests_mock.mock() as mock:
        mock.get('http://cms.com/api/pages/1/')
        client.get_page(1, draft_token='123')
        request = mock.request_history[0]

    assert request.qs == {'draft_token': ['123']}


def test_cms_client_language():
    client = helpers.DirectoryCMSClient(
        base_url='http://cms.com',
        api_key='debug',
    )
    with requests_mock.mock() as mock:
        mock.get('http://cms.com/api/pages/1/')
        client.get_page(1, language_code='de')
        request = mock.request_history[0]

    assert request.qs == {'lang': ['de']}


def test_cms_client_published():
    client = helpers.DirectoryCMSClient(
        base_url='http://cms.com',
        api_key='debug',
    )
    with requests_mock.mock() as mock:
        mock.get('http://cms.com/api/pages/2/')
        client.get_page(2)
        request = mock.request_history[0]

    assert request.qs == {}
