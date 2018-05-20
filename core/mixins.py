from django.conf import settings
from django.shortcuts import redirect
from django.utils import translation
from django.utils.cache import set_response_etag

from core import forms, helpers


class IncorrectSlug(Exception):
    def __init__(self, canonical_url, *args, **kwargs):
        self.canonical_url = canonical_url
        super().__init__(*args, **kwargs)


class SetEtagMixin:
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if request.method == 'GET':
            response.add_post_render_callback(set_response_etag)
        return response


class EnableTranslationsMixin:
    template_name_bidi = None
    language_form_class = forms.LanguageForm

    def __init__(self, *args, **kwargs):
        dependency = 'core.middleware.ForceDefaultLocale'
        assert dependency in settings.MIDDLEWARE_CLASSES
        super().__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        translation.activate(request.LANGUAGE_CODE)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['LANGUAGE_BIDI'] = translation.get_language_bidi()
        language_form_kwargs = self.get_language_form_kwargs()
        context['language_switcher'] = {
            'show': True,
            'form': self.language_form_class(**language_form_kwargs),
        }
        return context

    def get_language_form_kwargs(self, **kwargs):
        return {
            'initial': forms.get_language_form_initial_data(),
            **kwargs,
        }


class ActiveViewNameMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_view_name'] = self.active_view_name
        return context


class GetCMSPageMixin:

    def get_cms_page(self):
        response = helpers.cms_client.lookup_by_slug(
            slug=self.kwargs['slug'],
            draft_token=self.request.GET.get('draft_token'),
            language_code=translation.get_language(),
        )
        return self.handle_cms_response(response)

    def handle_cms_response(self, response):
        page = helpers.handle_cms_response(response)
        if page['meta']['slug'] != self.kwargs['slug']:
            raise IncorrectSlug(page['meta']['url'])
        return page

    def dispatch(self, *args, **kwargs):
        try:
            return super().dispatch(*args, **kwargs)
        except IncorrectSlug as exception:
            return redirect(exception.canonical_url)


class CMSLanguageSwitcherMixin:
    def get_context_data(self, page, *args, **kwargs):
        form = forms.LanguageForm(
            initial={'lang': translation.get_language()},
            language_choices=page['meta']['languages']
        )
        show_language_switcher = (
            len(page['meta']['languages']) > 1 and
            form.is_language_available(translation.get_language())
        )
        return super().get_context_data(
            page=page,
            language_switcher={'form': form, 'show': show_language_switcher},
            *args,
            **kwargs
        )
