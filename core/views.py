from directory_constants.constants import cms
from directory_cms_client.client import cms_api_client
import directory_forms_api_client.helpers

from django.conf import settings
from django.urls import reverse
from django.utils import translation
from django.utils.functional import cached_property
from django.template.response import TemplateResponse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView

from directory_api_client.client import api_client
from core import forms, helpers, mixins
from directory_components.mixins import CountryDisplayMixin


class ActivateTranslationMixin:
    def dispatch(self, *args, **kwargs):
        translation.activate(self.request.LANGUAGE_CODE)
        return super().dispatch(*args, **kwargs)


class LandingPageCMSView(
    mixins.CMSLanguageSwitcherMixin,
    mixins.ActiveViewNameMixin,
    mixins.GetCMSComponentMixin,
    ActivateTranslationMixin,
    CountryDisplayMixin,
    TemplateView
):
    active_view_name = 'index'
    template_name = 'core/landing-page.html'
    component_slug = cms.COMPONENTS_BANNER_INTERNATIONAL_SLUG

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            page=self.page,
            search_form=forms.SearchForm(),
            *args,
            **kwargs
        )

    @cached_property
    def page(self):
        response = cms_api_client.lookup_by_slug(
            slug=cms.FIND_A_SUPPLIER_LANDING_SLUG,
            language_code=translation.get_language(),
            draft_token=self.request.GET.get('draft_token'),
        )
        return helpers.handle_cms_response(response)


class RedirectToCMSIndustryView(RedirectView):
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        return reverse(
            'sector-detail-verbose', kwargs={'slug': self.kwargs['slug']}
        )


class LeadGenerationFormView(
    mixins.EnableTranslationsMixin, CountryDisplayMixin, FormView
):
    success_template = 'lead-generation-success.html'
    template_name = 'lead-generation.html'
    template_name_bidi = 'bidi/lead-generation.html'
    form_class = forms.LeadGenerationForm

    def form_valid(self, form):
        sender = directory_forms_api_client.helpers.Sender(
            email_address=form.cleaned_data['email_address'],
            country_code=form.cleaned_data['country'],
        )
        spam_control = directory_forms_api_client.helpers.SpamControl(
            contents=[form.cleaned_data['comment']]
        )
        response = form.save(
            email_address=form.cleaned_data['email_address'],
            full_name=form.cleaned_data['full_name'],
            subject=settings.ZENDESK_TICKET_SUBJECT,
            service_name=settings.DIRECTORY_FORMS_API_ZENDESK_SEVICE_NAME,
            form_url=self.request.path,
            sender=sender,
            spam_control=spam_control,
        )
        response.raise_for_status()
        return TemplateResponse(self.request, self.success_template)


class AnonymousSubscribeFormView(CountryDisplayMixin, FormView):
    success_template = 'anonymous-subscribe-success.html'
    template_name = 'anonymous-subscribe.html'
    form_class = forms.AnonymousSubscribeForm

    def form_valid(self, form):
        data = forms.serialize_anonymous_subscriber_forms(form.cleaned_data)
        response = api_client.buyer.send_form(data)
        response.raise_for_status()
        return TemplateResponse(self.request, self.success_template)
