import sys

from urllib.parse import urlsplit, urlunsplit
from django.http import HttpResponseRedirect

from django.conf import settings
from django.shortcuts import redirect


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
