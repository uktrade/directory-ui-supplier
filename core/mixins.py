from django.conf import settings
from django.utils import translation
from django.utils.cache import set_response_etag

from core import forms, helpers
from enrolment.forms import LanguageForm, get_language_form_initial_data


class SetEtagMixin:
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if request.method == 'GET':
            response.add_post_render_callback(set_response_etag)
        return response


class ConditionalEnableTranslationsMixin:
    translations_enabled = True
    template_name_bidi = None
    language_form_class = LanguageForm

    def __init__(self, *args, **kwargs):
        dependency = 'ui.middleware.ForceDefaultLocale'
        assert dependency in settings.MIDDLEWARE_CLASSES
        super().__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if self.translations_enabled:
            translation.activate(request.LANGUAGE_CODE)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['LANGUAGE_BIDI'] = translation.get_language_bidi()
        language_form_kwargs = self.get_language_form_kwargs()
        if self.translations_enabled:
            context['language_switcher'] = {
                'show': True,
                'form': self.language_form_class(**language_form_kwargs),
            }
        return context

    def get_language_form_kwargs(self, **kwargs):
        return {
            'initial': get_language_form_initial_data(),
            **kwargs,
        }

    def get_template_names(self):
        if translation.get_language_bidi():
            return [self.template_name_bidi]
        return super().get_template_names()


class ActiveViewNameMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_view_name'] = self.active_view_name
        return context


class GetCMSPageMixin:
    def get_cms_page(self):
        response = helpers.cms_client.get_page(
            page_id=self.kwargs['cms_page_id'],
            draft_token=self.request.GET.get('draft_token'),
            language_code=translation.get_language(),
        )
        return helpers.handle_cms_response(response)


class CMSLanguageSwitcherMixin:
    def get_context_data(self, page, *args, **kwargs):
        form = forms.LanguageForm(
            initial={'lang': translation.get_language()},
            language_choices=page['languages']
        )
        show_language_switcher = (
            len(page['languages']) > 1 and
            form.is_language_available(translation.get_language())
        )
        return super().get_context_data(
            page=page,
            language_switcher={'form': form, 'show': show_language_switcher},
            *args,
            **kwargs
        )
