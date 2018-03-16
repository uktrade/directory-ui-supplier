from directory_components.helpers import SocialLinkBuilder

from django.conf import settings
from django.shortcuts import Http404
from django.utils import translation
from django.views.generic import TemplateView

from core.helpers import cms_client
from core.mixins import SetEtagMixin
from enrolment.forms import LanguageIndustriesForm
from exportopportunity.helpers import get_showcase_companies
from ui.views import ConditionalEnableTranslationsMixin


class BaseCMSView(
    SetEtagMixin, ConditionalEnableTranslationsMixin, TemplateView
):

    def dispatch(self, *args, **kwargs):
        if not settings.FEATURE_CMS_ENABLED:
            raise Http404()
        return super().dispatch(*args, **kwargs)

    def get_cms_page(self, cms_page_id):
        response = cms_client.get_page(
            page_id=cms_page_id,
            draft_token=self.request.GET.get('draft_token'),
            language_code=translation.get_language(),
        )
        if response.status_code == 404:
            raise Http404()
        response.raise_for_status()
        return response.json()


class SectorDetailCMSView(BaseCMSView):
    language_form_class = LanguageIndustriesForm
    template_name = 'industry/sector-detail.html'

    def get_context_data(self, *args, **kwargs):
        page = self.get_cms_page(self.kwargs['cms_page_id'])
        return super().get_context_data(
            page=page,
            companies=self.get_companies(page['sector_value']),
            *args, **kwargs
        )

    def get_companies(self, sector_value):
        return get_showcase_companies(sectors=sector_value, size=6)


class SectorArticleCMSView(BaseCMSView):
    language_form_class = LanguageIndustriesForm
    template_name = 'industry/sector-article.html'

    def get_context_data(self, *args, **kwargs):
        page = self.get_cms_page(self.kwargs['cms_page_id'])
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
