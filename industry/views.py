from directory_components.helpers import SocialLinkBuilder

from django.conf import settings
from django.shortcuts import Http404
from django.utils import translation
from django.views.generic import TemplateView

from core.helpers import cms_client, handle_cms_response
from core.views import ActiveViewNameMixin, ConditionalEnableTranslationsMixin
from enrolment.forms import LanguageIndustriesForm
from exportopportunity.helpers import get_showcase_companies


class GetCMSPageMixin:
    def get_cms_page(self):
        response = cms_client.get_page(
            page_id=self.kwargs['cms_page_id'],
            draft_token=self.request.GET.get('draft_token'),
            language_code=translation.get_language(),
        )
        return handle_cms_response(response)


class BaseCMSView(ConditionalEnableTranslationsMixin, TemplateView):

    language_form_class = LanguageIndustriesForm

    def dispatch(self, *args, **kwargs):
        if not settings.FEATURE_CMS_ENABLED:
            raise Http404()
        return super().dispatch(*args, **kwargs)


class SectorDetailCMSView(GetCMSPageMixin, BaseCMSView):
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


class SectorArticleCMSView(GetCMSPageMixin, BaseCMSView):
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


class SectorLandingPageCMSView(ActiveViewNameMixin, BaseCMSView):
    active_view_name = 'sector-list'
    template_name = 'industry/list.html'

    def list_pages(self):
        response = cms_client.find_a_supplier.list_industry_pages(
            language_code=translation.get_language(),
            draft_token=self.request.GET.get('draft_token'),
        )
        return handle_cms_response(response)

    def get_cms_page(self):
        response = cms_client.find_a_supplier.get_industries_landing_page(
            language_code=translation.get_language(),
            draft_token=self.request.GET.get('draft_token'),
        )
        return handle_cms_response(response)

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            pages=self.list_pages()['items'],
            page=self.get_cms_page(),
            *args,
            **kwargs
        )
