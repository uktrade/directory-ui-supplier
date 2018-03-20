from django.conf import settings
from django.shortcuts import Http404

from directory_cms_client import DirectoryCMSClient


cms_client = DirectoryCMSClient(
    base_url=settings.CMS_URL,
    api_key=settings.CMS_SIGNATURE_SECRET,
)


def handle_cms_response(response):
    if response.status_code == 404:
        raise Http404()
    response.raise_for_status()
    return response.json()
