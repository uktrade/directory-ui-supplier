from django.middleware.locale import LocaleMiddleware
from django.utils import translation


class LocaleQuerystringMiddleware(LocaleMiddleware):
    def process_request(self, request):
        super().process_request(request)
        language_code = request.GET.get('lang')
        language_codes = translation.trans_real.get_languages()
        if language_code and language_code in language_codes:
            translation.activate(language_code)
            request.LANGUAGE_CODE = translation.get_language()
