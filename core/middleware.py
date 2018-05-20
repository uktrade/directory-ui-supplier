import sys

from urllib.parse import urlsplit, urlunsplit
from django.http import HttpResponseRedirect

from django.conf import settings
from django.middleware.locale import LocaleMiddleware
from django.shortcuts import redirect
from django.utils import translation

from core import helpers


class MaintenanceModeMiddleware:
    maintenance_url = 'https://sorry.great.gov.uk'

    def process_request(self, request):
        if settings.FEATURE_MAINTENANCE_MODE_ENABLED:
            return redirect(self.maintenance_url)


class SSLRedirectMiddleware:

    def process_request(self, request):
        if not request.is_secure():
            if "runserver" not in sys.argv and "test" not in sys.argv:
                return HttpResponseRedirect(urlunsplit(
                    ["https"] + list(urlsplit(request.get_raw_uri())[1:])))


class LocaleQuerystringMiddleware(LocaleMiddleware):

    def process_request(self, request):
        super().process_request(request)
        language_code = helpers.get_language_from_querystring(request)
        if language_code:
            translation.activate(language_code)
            request.LANGUAGE_CODE = translation.get_language()


class PersistLocaleMiddleware:
    def process_response(self, request, response):
        response.set_cookie(
            key=settings.LANGUAGE_COOKIE_NAME,
            value=translation.get_language(),
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path=settings.LANGUAGE_COOKIE_PATH,
            domain=settings.LANGUAGE_COOKIE_DOMAIN
        )
        return response


class ForceDefaultLocale:
    """
    Force translation to English before view is called, then putting the user's
    original language back after the view has been called, laying the ground
    work for`EnableTranslationsMixin` to turn on the desired locale. This
    provides per-view translations.

    """

    def process_request(self, request):
        translation.activate(settings.LANGUAGE_CODE)

    def process_response(self, request, response):
        if hasattr(request, 'LANGUAGE_CODE') and request.LANGUAGE_CODE:
            translation.activate(request.LANGUAGE_CODE)
        return response

    def process_exception(self, request, exception):
        if hasattr(request, 'LANGUAGE_CODE') and request.LANGUAGE_CODE:
            translation.activate(request.LANGUAGE_CODE)
