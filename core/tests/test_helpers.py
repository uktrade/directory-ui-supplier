import pytest
import requests
import requests_mock

from django.shortcuts import Http404

from core import helpers
import core.tests.helpers


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


@pytest.mark.parametrize('status_code,exception', (
    (400, requests.exceptions.HTTPError),
    (404, Http404),
    (500, requests.exceptions.HTTPError),
))
def test_handle_cms_response_error(status_code, exception):
    response = core.tests.helpers.create_response(status_code=status_code)
    with pytest.raises(exception):
        helpers.handle_cms_response(response)


def test_handle_cms_response_ok():
    response = core.tests.helpers.create_response(
        status_code=200, json_payload={'field': 'value'}
    )

    assert helpers.handle_cms_response(response) == {'field': 'value'}
