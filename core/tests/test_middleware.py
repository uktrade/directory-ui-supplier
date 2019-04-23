from django.conf import settings


def test_locale_middleware_installed():
    expected = 'core.middleware.LocaleQuerystringMiddleware'
    assert expected in settings.MIDDLEWARE_CLASSES
