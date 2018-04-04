import functools

from directory_components.helpers import SocialLinkBuilder

from django.conf import settings
from django.template.response import TemplateResponse
from django.utils import translation
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from core.helpers import cms_client, handle_cms_response
from core.views import CMSFeatureFlagMixin
from core.mixins import (
    ActiveViewNameMixin, GetCMSPageMixin, CMSLanguageSwitcherMixin
)
from exportopportunity.helpers import get_showcase_companies
from industry import forms
from zenpy import Zenpy
from zenpy.lib.api_objects import Ticket, User as ZendeskUser


ZENPY_CREDENTIALS = {
    'email': settings.ZENDESK_EMAIL,
    'token': settings.ZENDESK_TOKEN,
    'subdomain': settings.ZENDESK_SUBDOMAIN
}
# Zenpy will let the connection timeout after 5s and will retry 3 times
zenpy_client = Zenpy(timeout=5, **ZENPY_CREDENTIALS)


class IndustryDetailCMSView(
    CMSFeatureFlagMixin, CMSLanguageSwitcherMixin, GetCMSPageMixin,
    TemplateView
):
    template_name = 'industry/detail.html'

    def get_context_data(self, *args, **kwargs):
        page = self.get_cms_page()
        return super().get_context_data(
            page=page,
            companies=self.get_companies(page['sector_value']),
            *args, **kwargs
        )

    def get_companies(self, sector_value):
        return get_showcase_companies(sectors=sector_value, size=6)


class IndustryDetailContactCMSView(
    CMSFeatureFlagMixin, CMSLanguageSwitcherMixin, GetCMSPageMixin,
    FormView
):
    template_name = 'industry/contact.html'
    template_name_success = 'industry/contact-success.html'
    form_class = forms.ContactForm

    def get_context_data(self, *args, **kwargs):
        page = self.get_cms_page()
        return super().get_context_data(page=page, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial['sector'] = self.get_cms_page()['sector_value']
        return initial

    @functools.lru_cache()
    def get_cms_page(self):
        return super().get_cms_page()

    def form_valid(self, form):
        zendesk_user = self.get_or_create_zendesk_user(form.cleaned_data)
        self.create_zendesk_ticket(form.cleaned_data, zendesk_user)
        return TemplateResponse(
            self.request,
            self.template_name_success,
            self.get_context_data(),
        )

    @staticmethod
    def get_or_create_zendesk_user(cleaned_data):
        zendesk_user = ZendeskUser(
            name=cleaned_data['full_name'],
            email=cleaned_data['email_address'],
        )
        return zenpy_client.users.create_or_update(zendesk_user)

    @staticmethod
    def create_zendesk_ticket(cleaned_data, zendesk_user):
        description = [
            '{0}: {1}'.format(key.title().replace('_', ' '), value)
            for key, value in sorted(cleaned_data.items())
        ]
        ticket = Ticket(
            subject=cleaned_data['sector'] + ' contact form submitted.',
            description='\n'.join(description),
            submitter_id=zendesk_user.id,
            requester_id=zendesk_user.id,
        )
        zenpy_client.tickets.create(ticket)


class IndustryArticleCMSView(
    CMSFeatureFlagMixin, CMSLanguageSwitcherMixin, GetCMSPageMixin,
    TemplateView
):
    template_name = 'industry/article.html'

    def get_context_data(self, *args, **kwargs):
        page = self.get_cms_page()
        social_links_builder = SocialLinkBuilder(
            url=self.request.build_absolute_uri(),
            page_title=page['title'],
            app_title='Find A Supplier',
        )
        return super().get_context_data(
            page=page,
            social_links=social_links_builder.links,
            *args, **kwargs
        )


class IndustryLandingPageCMSView(
    CMSFeatureFlagMixin, CMSLanguageSwitcherMixin, ActiveViewNameMixin,
    TemplateView
):
    active_view_name = 'sector-list'
    template_name = 'industry/list.html'

    def get_cms_page(self):
        response = cms_client.find_a_supplier.get_industries_landing_page(
            language_code=translation.get_language(),
            draft_token=self.request.GET.get('draft_token'),
        )
        return handle_cms_response(response)

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            page=self.get_cms_page(),
            *args,
            **kwargs
        )
