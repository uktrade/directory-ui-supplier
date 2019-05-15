from directory_api_client.client import api_client
from directory_components.mixins import (
    CMSLanguageSwitcherMixin, CountryDisplayMixin, EnableTranslationsMixin,
    GA360Mixin)
from directory_constants import slugs
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

from core import forms, helpers, mixins


class LandingPageCMSView(
    CMSLanguageSwitcherMixin,
    mixins.ActiveViewNameMixin,
    mixins.GetCMSComponentMixin,
    CountryDisplayMixin,
    GA360Mixin,
    TemplateView
):
    active_view_name = 'index'
    template_name = 'core/landing-page.html'
    component_slug = slugs.COMPONENTS_BANNER_INTERNATIONAL
    ga360_payload = {'page_type': 'FindASupplierLandingPage'}

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
            slug=slugs.FIND_A_SUPPLIER_LANDING,
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
    EnableTranslationsMixin, CountryDisplayMixin, GA360Mixin, FormView
):
    success_template = 'lead-generation-success.html'
    template_name = 'lead-generation.html'
    template_name_bidi = 'bidi/lead-generation.html'
    form_class = forms.LeadGenerationForm
    ga360_payload = {'page_type': 'FindASupplierLeadGenerationForm'}

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


class AnonymousSubscribeFormView(CountryDisplayMixin, GA360Mixin, FormView):
    success_template = 'anonymous-subscribe-success.html'
    template_name = 'anonymous-subscribe.html'
    form_class = forms.AnonymousSubscribeForm
    ga360_payload = {'page_type': 'FindASupplierAnonymousSubscribeForm'}

    def form_valid(self, form):
        data = forms.serialize_anonymous_subscriber_forms(form.cleaned_data)
        response = api_client.buyer.send_form(data)
        response.raise_for_status()
        return TemplateResponse(self.request, self.success_template)


class SendContactNotifyMessagesMixin:

    def send_company_message(self, form):
        sender = directory_forms_api_client.helpers.Sender(
            email_address=form.cleaned_data['email_address'],
            country_code=None,
        )
        spam_control = directory_forms_api_client.helpers.SpamControl(
            contents=[form.cleaned_data['subject'], form.cleaned_data['body']]
        )

        response = form.save(
            template_id=self.notify_settings.contact_company_template,
            email_address=self.company['email_address'],
            form_url=self.request.path,
            sender=sender,
            spam_control=spam_control,
        )
        response.raise_for_status()

    def send_support_message(self, form):
        response = form.save(
            template_id=self.notify_settings.contact_support_template,
            email_address=self.notify_settings.contact_support_email_address,
            form_url=self.request.get_full_path(),
        )
        response.raise_for_status()

    def send_investor_message(self, form):
        spam_control = directory_forms_api_client.helpers.SpamControl(
            contents=[form.cleaned_data['subject'], form.cleaned_data['body']]
        )
        response = form.save(
            template_id=self.notify_settings.contact_investor_template,
            email_address=form.cleaned_data['email_address'],
            company_email=self.company['email_address'],
            form_url=self.request.get_full_path(),
            spam_control=spam_control,
        )
        response.raise_for_status()

    def form_valid(self, form):
        self.send_company_message(form)
        self.send_support_message(form)
        self.send_investor_message(form)
        return super().form_valid(form)


class BaseNotifyFormView(SendContactNotifyMessagesMixin, FormView):
    pass
