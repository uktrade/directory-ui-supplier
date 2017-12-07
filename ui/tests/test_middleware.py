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


def test_locale_persist_middleware_installed():
    expected = 'ui.middleware.PersistLocaleMiddleware'
    assert expected in settings.MIDDLEWARE_CLASSES


def test_locale_persist_middleware_handles_no_explicit_language(client, rf):
    request = rf.get('/')
    response = HttpResponse()
    request.session = client.session
    instance = middleware.PersistLocaleMiddleware()

    instance.process_response(request, response)

    cookie = response.cookies[settings.LANGUAGE_COOKIE_NAME]
    assert cookie.value == settings.LANGUAGE_CODE


def test_locale_persist_middleware_persists_explicit_language(client, rf):
    language_code = 'en-gb'
    request = rf.get('/', {'lang': language_code})
    response = HttpResponse()
    request.session = client.session
    instance = middleware.PersistLocaleMiddleware()

    instance.process_response(request, response)
    cookie = response.cookies[settings.LANGUAGE_COOKIE_NAME]

    assert cookie.value == language_code


def test_force_default_locale_installed():
    assert 'ui.middleware.ForceDefaultLocale' in settings.MIDDLEWARE_CLASSES


def test_force_default_locale_no_language_in_request(rf, settings):
    request = rf.get('/')
    instance = middleware.ForceDefaultLocale()

    assert not hasattr(request, 'LANGUAGE_CODE')

    instance.process_request(request)


def test_force_default_locale_sets_to_english(rf, settings):
    request = rf.get('/')
    instance = middleware.ForceDefaultLocale()

    translation.activate('de')

    assert translation.get_language() == 'de'
    instance.process_request(request)
    assert translation.get_language() == settings.LANGUAGE_CODE


def test_force_default_locale_sets_to_prevous_on_exception(rf):
    request = rf.get('/')
    request.LANGUAGE_CODE = 'de'
    instance = middleware.ForceDefaultLocale()

    translation.activate('de')
    assert translation.get_language() == 'de'

    instance.process_request(request)
    assert translation.get_language() == settings.LANGUAGE_CODE

    instance.process_exception(request, None)
    assert translation.get_language() == 'de'


def test_force_default_locale_sets_to_prevous_on_response(rf):
    request = rf.get('/')
    request.LANGUAGE_CODE = 'de'
    instance = middleware.ForceDefaultLocale()

    translation.activate('de')
    assert translation.get_language() == 'de'

    instance.process_request(request)
    assert translation.get_language() == settings.LANGUAGE_CODE

    instance.process_response(request, None)
    assert translation.get_language() == 'de'
