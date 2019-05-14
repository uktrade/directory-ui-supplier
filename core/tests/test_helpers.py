import pytest
import requests

from django.shortcuts import Http404
from django.urls import reverse

from core import helpers
import core.tests.helpers


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


@pytest.mark.parametrize('path,expect_code', (
    ('/', None),
    ('?language=pt', 'pt'),
    ('/?language=ar', 'ar'),
    ('/industries?language=es', 'es'),
    ('/industries/?language=zh-hans', 'zh-hans'),
    ('/industries/aerospace?language=de', 'de'),
    ('/industries/automotive/?language=fr', 'fr'),
    ('?lang=fr', 'fr'),
    ('?language=de&lang=de', 'de'),
    ('?lang=pt&language=es', 'es')
))
def test_get_language_from_querystring(path, expect_code, rf):
    url = reverse('index')
    request = rf.get(url + path)
    language_code = helpers.get_language_from_querystring(request)
    assert language_code == expect_code
