import functools

from directory_constants.constants import cms
from directory_components.helpers import SocialLinkBuilder

from django.conf import settings
from django.utils import translation
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse, reverse_lazy

from directory_cms_client.client import cms_api_client

from core.views import ActivateTranslationMixin
from core.mixins import (
    ActiveViewNameMixin,
    CMSLanguageSwitcherMixin,
    GetCMSPageMixin,
    SpecificRefererRequiredMixin
)
from core.helpers import handle_cms_response
from industry import forms
from industry.helpers import get_showcase_companies


class IndustryDetailCMSView(
    ActivateTranslationMixin, CMSLanguageSwitcherMixin, GetCMSPageMixin,
    TemplateView
):
    template_name = 'industry/detail.html'

    def get_context_data(self, *args, **kwargs):
        page = self.get_cms_page()
        companies = self.get_companies(
            sector_values=page['search_filter_sector'],
            term=page['search_filter_text'],
            search_filter_showcase_only=page['search_filter_showcase_only']
        )
        return super().get_context_data(
            page=page, companies=companies, *args, **kwargs
        )

    @staticmethod
    def get_companies(sector_values, term, search_filter_showcase_only):
        kwargs = {'size': 6}
        if sector_values:
            kwargs['sectors'] = sector_values
        if term:
            kwargs['term'] = term
        if search_filter_showcase_only:
            kwargs['is_showcase_company'] = True
        return get_showcase_companies(**kwargs)


class GetContactPageMixin:
    @functools.lru_cache()
    def get_contact_page(self):
        response = cms_api_client.lookup_by_slug(
            slug=cms.FIND_A_SUPPLIER_INDUSTRY_CONTACT_SLUG,
            language_code=translation.get_language(),
            draft_token=self.request.GET.get('draft_token'),
        )
        return handle_cms_response(response)

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            page=self.get_contact_page(),
            *args, **kwargs
        )


class GetIndustryPageMixin:
    @functools.lru_cache()
    def get_industry_page(self):
        response = cms_api_client.lookup_by_slug(
            slug=self.kwargs['slug'],
            language_code=translation.get_language(),
        )
        return self.handle_cms_response(response)

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            industry_page=self.get_industry_page(),
            *args, **kwargs
        )


class BaseIndustryContactView(FormView):

    template_name = 'industry/contact.html'
    form_class = forms.ContactForm

    def get_form_kwargs(self, *args, **kwargs):
        industry_choices = [
            (item['meta']['slug'], item['breadcrumbs_label'])
            for item in self.get_contact_page()['industry_options']
        ]
        return {
            **super().get_form_kwargs(*args, **kwargs),
            'industry_choices': industry_choices,
        }

    def form_valid(self, form):
        response = form.save(
            email_address=form.cleaned_data['email_address'],
            full_name=form.cleaned_data['full_name'],
            subject=form.cleaned_data['sector'] + ' contact form submitted.',
            service_name=settings.DIRECTORY_FORMS_API_ZENDESK_SEVICE_NAME,
            form_url=self.request.path,
        )
        response.raise_for_status()
        return super().form_valid(form)


class IndustryDetailContactCMSView(
    ActivateTranslationMixin, GetIndustryPageMixin, GetCMSPageMixin,
    GetContactPageMixin, CMSLanguageSwitcherMixin, BaseIndustryContactView
):

    def get_success_url(self):
        return reverse('sector-detail-cms-contact-sent', kwargs=self.kwargs)

    def get_initial(self):
        initial = super().get_initial()
        page = self.get_industry_page()
        initial['sector'] = page['meta']['slug']
        return initial


class IndustryLandingPageContactCMSView(
    ActivateTranslationMixin, GetCMSPageMixin, GetContactPageMixin,
    CMSLanguageSwitcherMixin, BaseIndustryContactView
):
    success_url = reverse_lazy('sector-list-cms-contact-sent')


class IndustryDetailContactCMSSentView(
    ActivateTranslationMixin, SpecificRefererRequiredMixin, GetCMSPageMixin,
    GetContactPageMixin, GetIndustryPageMixin, TemplateView
):
    template_name = 'industry/contact-success.html'

    @property
    def expected_referer_url(self):
        return reverse('sector-detail-cms-contact', kwargs=self.kwargs)


class IndustryLandingPageContactCMSSentView(
    ActivateTranslationMixin, SpecificRefererRequiredMixin, GetCMSPageMixin,
    GetContactPageMixin, TemplateView
):
    template_name = 'industry/contact-success.html'

    @property
    def expected_referer_url(self):
        return reverse('sector-list-cms-contact')


class IndustryArticleCMSView(
    ActivateTranslationMixin, CMSLanguageSwitcherMixin, GetCMSPageMixin,
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
    ActivateTranslationMixin, CMSLanguageSwitcherMixin, ActiveViewNameMixin,
    TemplateView
):
    active_view_name = 'sector-list'
    template_name = 'industry/list.html'

    def get_cms_page(self):
        response = cms_api_client.lookup_by_slug(
            slug=cms.FIND_A_SUPPLIER_INDUSTRY_LANDING_SLUG,
            language_code=translation.get_language(),
            draft_token=self.request.GET.get('draft_token'),
        )
        return handle_cms_response(response)

    def get_context_data(self, *args, **kwargs):
        page = self.get_cms_page()
        showcase_industries = self.get_showcase_industries(page['industries'])
        return super().get_context_data(
            page=page,
            showcase_industries=showcase_industries,
            *args,
            **kwargs
        )

    @staticmethod
    def get_showcase_industries(industries):
        showcase_industries = [
            industry for industry in industries
            if industry['show_on_industries_showcase_page']
        ]
        return showcase_industries or industries[:9]
