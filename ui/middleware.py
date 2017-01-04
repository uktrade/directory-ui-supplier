from django.conf import settings
from django.middleware.locale import LocaleMiddleware
from django.utils import translation


class LocaleQuerystringMiddleware(LocaleMiddleware):
    def process_request(self, request):
        # from ipdb import set_trace; set_trace()
        super().process_request(request)
        language_code = request.GET.get('lang')
        language_codes = translation.trans_real.get_languages()
        if language_code and language_code in language_codes:
            translation.activate(language_code)
            request.LANGUAGE_CODE = translation.get_language()


class PersistLocaleMiddleware:
    def process_response(self, request, response):
        language_code = translation.get_language()
        # django.middleware.locale.LocaleMiddleware checks activates the
        # language code in request.COOKIES[settings.LANGUAGE_COOKIE_NAME]
        if language_code:
            response.set_cookie(
                key=settings.LANGUAGE_COOKIE_NAME,
                value=language_code,
                max_age=settings.LANGUAGE_COOKIE_AGE,
                path=settings.LANGUAGE_COOKIE_PATH,
                domain=settings.LANGUAGE_COOKIE_DOMAIN
            )
        return response
