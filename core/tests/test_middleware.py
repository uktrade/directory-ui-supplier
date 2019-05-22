from django.conf import settings
from core.middleware import PrefixUrlMiddleware


def test_locale_middleware_installed():
    expected = 'directory_components.middleware.LocaleQuerystringMiddleware'
    assert expected in settings.MIDDLEWARE_CLASSES


def test_prefix_url_middleware_investment_support_directory(rf):
    request = rf.get('/investment-support-directory/')
    response = PrefixUrlMiddleware().process_request(request)
    assert response is None


def test_prefix_url_middleware_to_trade(rf):
    request = rf.get('/feedback/')

    response = PrefixUrlMiddleware().process_request(request)
    assert response.status_code == 302
    prefix = PrefixUrlMiddleware().prefix
    assert response.url == f"{prefix}feedback/"
