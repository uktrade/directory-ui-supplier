from zenpy import Zenpy
from zenpy.lib.api_objects import Ticket, User as ZendeskUser

from django.conf import settings
from django.shortcuts import redirect, Http404
from django.template.response import TemplateResponse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from api_client import api_client
from enrolment import constants, forms
from core.views import ActiveViewNameMixin, ConditionalEnableTranslationsMixin
import industry.views


ZENPY_CREDENTIALS = {
    'email': settings.ZENDESK_EMAIL,
    'token': settings.ZENDESK_TOKEN,
    'subdomain': settings.ZENDESK_SUBDOMAIN
}
# Zenpy will let the connection timeout after 5s and will retry 3 times
zenpy_client = Zenpy(timeout=5, **ZENPY_CREDENTIALS)



class LeadGenerationFormView(ConditionalEnableTranslationsMixin, FormView):
    success_template = 'lead-generation-success.html'
    template_name = 'lead-generation.html'
    template_name_bidi = 'bidi/lead-generation.html'
    form_class = forms.LeadGenerationForm

    @property
    def translations_enabled(self):
        return (
            self.request.LANGUAGE_CODE not in
            settings.DISABLED_LANGUAGES_INDUSTRIES_PAGE
        )

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
        api_client.buyer.send_form(data)
        return TemplateResponse(self.request, self.success_template)


class LandingView(
    ActiveViewNameMixin, ConditionalEnableTranslationsMixin, TemplateView
):
    template_name = 'landing-page.html'
    template_name_bidi = 'bidi/landing-page.html'
    active_view_name = 'index'


class SectorListView(
    ActiveViewNameMixin, ConditionalEnableTranslationsMixin, TemplateView
):
    @classmethod
    def as_view(cls, *args, **kwargs):
        if settings.FEATURE_CMS_ENABLED:
            return industry.views.SectorLandingPageCMSView.as_view(
                *args, **kwargs
            )
        return super().as_view(*args, **kwargs)

    template_name = 'sector-list.html'
    template_name_bidi = 'bidi/sector-list.html'
    language_form_class = forms.LanguageIndustriesForm
    active_view_name = 'sector-list'

    @property
    def translations_enabled(self):
        return (
            self.request.LANGUAGE_CODE not in
            settings.DISABLED_LANGUAGES_INDUSTRIES_PAGE
        )


class PrivacyCookiesView(TemplateView):
    template_name = 'privacy-and-cookies.html'


class TermsView(TemplateView):
    template_name = 'terms-and-conditions.html'


class SectorDetailView(ConditionalEnableTranslationsMixin, TemplateView):
    template_name_bidi = None
    language_form_class = forms.LanguageIndustriesForm

    @property
    def translations_enabled(self):
        return (
            self.request.LANGUAGE_CODE not in
            settings.DISABLED_LANGUAGES_INDUSTRIES_PAGE
        )

    @classmethod
    def get_active_pages(cls):
        pages = {
            'health': {
                'template': 'marketing-pages/health.html',
                'context': constants.HEALTH_SECTOR_CONTEXT,
                'is_active': True,
            },
            'tech': {
                'template': 'marketing-pages/tech.html',
                'context': constants.TECH_SECTOR_CONTEXT,
                'is_active': True,
            },
            'creative': {
                'template': 'marketing-pages/creative.html',
                'context': constants.CREATIVE_SECTOR_CONTEXT,
                'is_active': True,
            },
            'food-and-drink': {
                'template': 'marketing-pages/food.html',
                'context': constants.FOOD_SECTOR_CONTEXT,
                'is_active': True,
            },
            'advanced-manufacturing': {
                'template': 'marketing-pages/advanced-manufacturing.html',
                'context': constants.ADVANCED_MANUFACTURING_CONTEXT,
                'is_active': settings.FEATURE_ADVANCED_MANUFACTURING_ENABLED,
            },
            'global-sports-infrastructure': {
                'template': 'marketing-pages/sports-infrastructure.html',
                'context': constants.GLOBAL_SPORTS_INFRASTRUCTURE_CONTEXT,
                'is_active': settings.FEATURE_SPORTS_INFRASTRUCTURE_ENABLED,
            }
        }
        return {key: val for key, val in pages.items() if val['is_active']}

    def dispatch(self, request, *args, **kwargs):
        # handling legacy "show summary/verbose description" url: ED-1471
        if 'verbose' in self.request.GET:
            return redirect('sector-detail-verbose', slug=self.kwargs['slug'])
        if self.kwargs['slug'] not in self.get_active_pages():
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        pages = self.get_active_pages()
        template_name = pages[self.kwargs['slug']]['template']
        return [template_name]

    def get_context_data(self, *args, **kwargs):
        pages = self.get_active_pages()
        context = super().get_context_data(*args, **kwargs)
        context.update(pages[self.kwargs['slug']]['context'])
        context['show_proposition'] = self.kwargs['show_proposition']
        context['slug'] = self.kwargs['slug']
        return context
