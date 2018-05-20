from directory_cms_client import constants as cms_constants
from zenpy import Zenpy
from zenpy.lib.api_objects import Ticket, User as ZendeskUser

from django.conf import settings
from django.urls import reverse
from django.utils import translation
from django.template.response import TemplateResponse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView

from api_client import api_client
from core import forms, helpers, mixins


ZENPY_CREDENTIALS = {
    'email': settings.ZENDESK_EMAIL,
    'token': settings.ZENDESK_TOKEN,
    'subdomain': settings.ZENDESK_SUBDOMAIN
}
# Zenpy will let the connection timeout after 5s and will retry 3 times
zenpy_client = Zenpy(timeout=5, **ZENPY_CREDENTIALS)


class CMSFeatureFlagMixin:
    def dispatch(self, *args, **kwargs):
        translation.activate(self.request.LANGUAGE_CODE)
        return super().dispatch(*args, **kwargs)


class LandingPageCMSView(
    mixins.CMSLanguageSwitcherMixin, mixins.ActiveViewNameMixin,
    CMSFeatureFlagMixin, TemplateView
):
    active_view_name = 'index'
    template_name = 'core/landing-page.html'

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            page=self.get_cms_page(),
            search_form=forms.SearchForm(),
            *args,
            **kwargs
        )

    def get_cms_page(self):
        response = helpers.cms_client.lookup_by_slug(
            slug=cms_constants.FIND_A_SUPPLIER_LANDING_SLUG,
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
    mixins.EnableTranslationsMixin, FormView
):
    success_template = 'lead-generation-success.html'
    template_name = 'lead-generation.html'
    template_name_bidi = 'bidi/lead-generation.html'
    form_class = forms.LeadGenerationForm

    def get_or_create_zendesk_user(self, cleaned_data):
        zendesk_user = ZendeskUser(
            name=cleaned_data['full_name'],
            email=cleaned_data['email_address'],
        )
        return zenpy_client.users.create_or_update(zendesk_user)

    def create_zendesk_ticket(self, cleaned_data, zendesk_user):
        description = (
            'Name: {full_name}\n'
            'Email: {email_address}\n'
            'Company: {company_name}\n'
            'Country: {country}\n'
            'Comment: {comment}'
        ).format(**cleaned_data)
        ticket = Ticket(
            subject=settings.ZENDESK_TICKET_SUBJECT,
            description=description,
            submitter_id=zendesk_user.id,
            requester_id=zendesk_user.id,
        )
        zenpy_client.tickets.create(ticket)

    def form_valid(self, form):
        zendesk_user = self.get_or_create_zendesk_user(form.cleaned_data)
        self.create_zendesk_ticket(form.cleaned_data, zendesk_user)
        return TemplateResponse(self.request, self.success_template)


class AnonymousSubscribeFormView(FormView):
    success_template = 'anonymous-subscribe-success.html'
    template_name = 'anonymous-subscribe.html'
    form_class = forms.AnonymousSubscribeForm

    def form_valid(self, form):
        data = forms.serialize_anonymous_subscriber_forms(form.cleaned_data)
        response = api_client.buyer.send_form(data)
        response.raise_for_status()
        return TemplateResponse(self.request, self.success_template)
