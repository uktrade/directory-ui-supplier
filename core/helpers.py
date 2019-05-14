from django.shortcuts import Http404
from django.utils import translation


def handle_cms_response(response):
    if response.status_code == 404:
        raise Http404()
    response.raise_for_status()
    return response.json()


def get_language_from_querystring(request):
    language_code = request.GET.get('language') or request.GET.get('lang')
    language_codes = translation.trans_real.get_languages()
    if language_code and language_code in language_codes:
        return language_code
