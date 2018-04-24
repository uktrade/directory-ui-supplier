import pytest
import requests

from django.shortcuts import Http404

from core import helpers
import core.tests.helpers


def test_cms_secrets(settings):
    assert helpers.cms_client.base_url == settings.CMS_URL
    assert (
        helpers.cms_client.request_signer.secret ==
        settings.CMS_SIGNATURE_SECRET
    )


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
