from directory_components.helpers import SocialLinkBuilder

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
    form_class = forms.ContactForm

    def get_context_data(self, *args, **kwargs):
        page = self.get_cms_page()
        return super().get_context_data(page=page, *args, **kwargs)


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
