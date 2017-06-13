from zenpy import Zenpy
from zenpy.lib.api_objects import Ticket, User as ZendeskUser

from django.conf import settings
from django.shortcuts import Http404
from django.template.response import TemplateResponse
from django.utils import translation
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from api_client import api_client
from enrolment import constants, forms


ZENPY_CREDENTIALS = {
    'email': settings.ZENDESK_EMAIL,
    'token': settings.ZENDESK_TOKEN,
    'subdomain': settings.ZENDESK_SUBDOMAIN
}
# Zenpy will let the connection timeout after 5s and will retry 3 times
zenpy_client = Zenpy(timeout=5, **ZENPY_CREDENTIALS)


class ConditionalEnableTranslationsMixin:

    translations_enabled = True
    template_name_bidi = None
    language_form_class = forms.LanguageForm

    def __init__(self, *args, **kwargs):
        dependency = 'ui.middleware.ForceDefaultLocale'
        assert dependency in settings.MIDDLEWARE_CLASSES

    def dispatch(self, request, *args, **kwargs):
        if self.translations_enabled:
            translation.activate(request.LANGUAGE_CODE)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['LANGUAGE_BIDI'] = translation.get_language_bidi()
        if self.translations_enabled:
            context['language_switcher'] = {
                'show': True,
                'form': self.language_form_class(
                    initial=forms.get_language_form_initial_data(),
                )
            }
        return context

    def get_template_names(self):
        if translation.get_language_bidi():
            return [self.template_name_bidi]
        return super().get_template_names()


class LeadGenerationFormView(ConditionalEnableTranslationsMixin, FormView):
    success_template = 'lead-generation-success.html'
    template_name = 'lead-generation.html'
    template_name_bidi = 'lead-generation.html'
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


class InternationalLandingView(ConditionalEnableTranslationsMixin,
                               TemplateView):
    template_name = 'landing-page.html'
    template_name_bidi = 'bidi/landing-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_view_name'] = 'index'
        return context


class InternationalLandingSectorListView(ConditionalEnableTranslationsMixin,
                                         TemplateView):
    template_name = 'landing-page-international-sector-list.html'
    template_name_bidi = 'bidi/landing-page-international-sector-list.html'
    language_form_class = forms.LanguageIndustriesForm

    @property
    def translations_enabled(self):
        return (
            self.request.LANGUAGE_CODE not in
            settings.DISABLED_LANGUAGES_INDUSTRIES_PAGE
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_view_name'] = 'international-sector-list'
        return context


class PrivacyCookiesView(TemplateView):
    template_name = 'privacy-and-cookies.html'


class TermsView(TemplateView):
    template_name = 'terms-and-conditions.html'


class InternationalLandingSectorDetailView(ConditionalEnableTranslationsMixin,
                                           TemplateView):

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
        context['show_proposition'] = 'verbose' in self.request.GET
        context['slug'] = self.kwargs['slug']
        return context
