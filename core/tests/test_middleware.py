from django.conf import settings


def test_locale_middleware_installed():
    expected = 'directory_components.middleware.LocaleQuerystringMiddleware'
    assert expected in settings.MIDDLEWARE_CLASSES
