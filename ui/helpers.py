from django.utils import translation


def get_language_from_querystring(request):
    language_code = request.GET.get('lang')
    language_codes = translation.trans_real.get_languages()
    if language_code and language_code in language_codes:
        return language_code
