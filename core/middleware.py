import sys
from urllib.parse import urlsplit, urlunsplit

from directory_components.middleware import AbstractPrefixUrlMiddleware

from django.http import HttpResponseRedirect
from django.middleware.locale import LocaleMiddleware
from django.utils import translation

from core import helpers


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


class PrefixUrlMiddleware(AbstractPrefixUrlMiddleware):
    prefix = '/trade/'
