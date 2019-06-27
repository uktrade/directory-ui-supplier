from directory_components.mixins import (
    CMSLanguageSwitcherMixin, CountryDisplayMixin, GA360Mixin
)
from directory_constants import slugs
from directory_cms_client import cms_api_client
import directory_forms_api_client.helpers

from django.urls import reverse
from django.utils import translation
from django.utils.functional import cached_property
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

    def __init__(self):
        super().__init__()

        self.set_ga360_payload(
            page_id='FindASupplierLandingPage',
            business_unit='FindASupplier',
            site_section='HomePage',
        )

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
            template_id=self.notify_settings.company_template,
            email_address=self.company['email_address'],
            form_url=self.request.path,
            sender=sender,
            spam_control=spam_control,
        )
        response.raise_for_status()

    def send_support_message(self, form):
        response = form.save(
            template_id=self.notify_settings.support_template,
            email_address=self.notify_settings.support_email_address,
            form_url=self.request.get_full_path(),
        )
        response.raise_for_status()

    def send_investor_message(self, form):
        spam_control = directory_forms_api_client.helpers.SpamControl(
            contents=[form.cleaned_data['subject'], form.cleaned_data['body']]
        )
        response = form.save(
            template_id=self.notify_settings.investor_template,
            email_address=form.cleaned_data['email_address'],
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
