from django.conf import settings
from django.http import HttpResponse
from django.utils import translation

from ui import middleware


def test_locale_middleware_installed():
    expected = 'ui.middleware.LocaleQuerystringMiddleware'
    assert expected in settings.MIDDLEWARE_CLASSES


def test_locale_middleware_sets_querystring_language(rf):
    request = rf.get('/', {'lang': 'en-gb'})
    instance = middleware.LocaleQuerystringMiddleware()

    instance.process_request(request)

    expected = 'en-gb'
    assert request.LANGUAGE_CODE == expected == translation.get_language()


def test_locale_middleware_ignored_invalid_querystring_language(rf):
    request = rf.get('/', {'lang': 'plip'})
    instance = middleware.LocaleQuerystringMiddleware()

    instance.process_request(request)

    expected = settings.LANGUAGE_CODE
    assert request.LANGUAGE_CODE == expected == translation.get_language()


def test_locale_middleware_handles_missing_querystring_language(rf):
    request = rf.get('/')
    instance = middleware.LocaleQuerystringMiddleware()

    instance.process_request(request)

    expected = settings.LANGUAGE_CODE
    assert request.LANGUAGE_CODE == expected == translation.get_language()


def test_persist_language_middleware_installed():
    expected = 'ui.middleware.PersistLocaleMiddleware'
    assert expected in settings.MIDDLEWARE_CLASSES


def test_persist_language_middleware_handles_no_explcit_language(client, rf):
    language_code = settings.LANGUAGE_CODE
    request = rf.get('/')
    response = HttpResponse()
    request.session = client.session
    instance = middleware.PersistLocaleMiddleware()

    instance.process_response(request, response)
    cookie = response.cookies[settings.LANGUAGE_COOKIE_NAME]

    assert cookie.value == language_code


def test_persist_language_middleware_persists_explcit_language(client, rf):
    language_code = 'en-gb'
    request = rf.get('/', {'lang': language_code})
    response = HttpResponse()
    request.session = client.session
    instance = middleware.PersistLocaleMiddleware()

    instance.process_response(request, response)
    cookie = response.cookies[settings.LANGUAGE_COOKIE_NAME]

    assert cookie.value == language_code
