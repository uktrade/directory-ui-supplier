import functools

import directory_forms_api_client.helpers
from directory_constants import cms, slugs
from directory_components.helpers import SocialLinkBuilder
from directory_components.mixins import (
    CMSLanguageSwitcherMixin, CountryDisplayMixin,
    GA360Mixin)

from django.conf import settings
from django.shortcuts import redirect
from django.utils import translation
from django.utils.functional import cached_property
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse, reverse_lazy

from directory_cms_client import cms_api_client

from core.mixins import (
    ActiveViewNameMixin,
    GetCMSPageMixin,
    SpecificRefererRequiredMixin
)
from core.helpers import handle_cms_response
from industry import forms
from industry.helpers import get_showcase_companies


class IndustryDetailCMSView(
    CMSLanguageSwitcherMixin,
    GetCMSPageMixin,
    CountryDisplayMixin,
    GA360Mixin,
    TemplateView
):
    template_name = 'industry/detail.html'

    def __init__(self):
        super().__init__()

        self.set_ga360_payload(
            page_id='FindASupplierIndustryDetail',
            business_unit='FindASupplier',
            site_section='Industries',
            site_subsection='Detail'
        )

    def get_context_data(self, *args, **kwargs):
        companies = self.get_companies(
            sector_values=self.page['search_filter_sector'],
            term=self.page['search_filter_text'],
            search_filter_showcase_only=(
                self.page['search_filter_showcase_only']
            )
        )
        return super().get_context_data(
            page=self.page, companies=companies, *args, **kwargs
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

    @cached_property
    def international_industry_page(self):
        response = cms_api_client.lookup_by_slug(
            slug=self.kwargs['slug'],
            language_code=translation.get_language(),
            draft_token=self.request.GET.get('draft_token'),
            service_name=cms.GREAT_INTERNATIONAL
        )
        if response.status_code == 200:
            return response.json()
        return None

    def dispatch(self, request, *args, **kwargs):
        page = self.international_industry_page
        if page:
            return redirect(page['full_url'])
        return super().dispatch(request, *args, **kwargs)


class GetCMSContactPageMixin:
    @functools.lru_cache()
    def get_contact_page(self):
        response = cms_api_client.lookup_by_slug(
            slug=slugs.FIND_A_SUPPLIER_INDUSTRY_CONTACT,
            language_code=translation.get_language(),
            draft_token=self.request.GET.get('draft_token'),
        )
        return handle_cms_response(response)

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            page=self.get_contact_page(),
            *args, **kwargs
        )

    @cached_property
    def page(self):
        return self.get_contact_page()


class GetIndustryPageMixin:
    @functools.lru_cache()
    def get_industry_page(self):
        response = cms_api_client.lookup_by_slug(
            slug=self.kwargs['slug'],
            language_code=translation.get_language(),
        )
        return handle_cms_response(response)

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            industry_page=self.get_industry_page(),
            *args, **kwargs
        )


class BaseIndustryContactView(CountryDisplayMixin, GA360Mixin, FormView):

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

    def send_agent_email(self, form):
        sender = directory_forms_api_client.helpers.Sender(
            email_address=form.cleaned_data['email_address'],
            country_code=form.cleaned_data['country'],
        )
        spam_control = directory_forms_api_client.helpers.SpamControl(
            contents=[form.cleaned_data['body']]
        )
        response = form.save(
            form_url=self.request.path,
            email_address=settings.CONTACT_INDUSTRY_AGENT_EMAIL_ADDRESS,
            template_id=settings.CONTACT_INDUSTRY_AGENT_TEMPLATE_ID,
            sender=sender,
            spam_control=spam_control,
        )
        response.raise_for_status()

    def send_user_email(self, form):
        response = form.save(
            form_url=self.request.path,
            email_address=form.cleaned_data['email_address'],
            template_id=settings.CONTACT_INDUSTRY_USER_TEMPLATE_ID,
            email_reply_to_id=settings.CONTACT_INDUSTRY_USER_REPLY_TO_ID,
        )
        response.raise_for_status()

    def form_valid(self, form):
        self.send_agent_email(form)
        self.send_user_email(form)
        return super().form_valid(form)


class IndustryDetailContactCMSView(
    GetIndustryPageMixin, GetCMSContactPageMixin,
    CMSLanguageSwitcherMixin, BaseIndustryContactView
):

    def __init__(self):
        super().__init__()

        self.set_ga360_payload(
            page_id='FindASupplierIndustryDetailContact',
            business_unit='FindASupplier',
            site_section='Industries',
            site_subsection='DetailContact'
        )

    def get_success_url(self):
        return reverse('sector-detail-cms-contact-sent', kwargs=self.kwargs)

    def get_initial(self):
        initial = super().get_initial()
        page = self.get_industry_page()
        initial['sector'] = page['meta']['slug']
        return initial


class IndustryLandingPageContactCMSView(
    GetCMSContactPageMixin, CMSLanguageSwitcherMixin,
    BaseIndustryContactView
):
    success_url = reverse_lazy('sector-list-cms-contact-sent')

    def __init__(self):
        super().__init__()

        self.set_ga360_payload(
            page_id='FindASupplierIndustryLandingPageContact',
            business_unit='FindASupplier',
            site_section='Industries',
            site_subsection='LandingPageContact'
        )


class IndustryDetailContactCMSSentView(
    CMSLanguageSwitcherMixin, SpecificRefererRequiredMixin,
    GetCMSContactPageMixin, GetIndustryPageMixin, CountryDisplayMixin,
    GA360Mixin, TemplateView
):
    template_name = 'industry/contact-success.html'

    def __init__(self):
        super().__init__()

        self.set_ga360_payload(
            page_id='FindASupplierIndustryDetailContactSent',
            business_unit='FindASupplier',
            site_section='Industries',
            site_subsection='DetailContactSent'
        )

    @property
    def expected_referer_url(self):
        return reverse('sector-detail-cms-contact', kwargs=self.kwargs)


class IndustryLandingPageContactCMSSentView(
    CMSLanguageSwitcherMixin, SpecificRefererRequiredMixin,
    GetCMSContactPageMixin, CountryDisplayMixin, GA360Mixin, TemplateView
):
    template_name = 'industry/contact-success.html'

    def __init__(self):
        super().__init__()

        self.set_ga360_payload(
            page_id='FindASupplierIndustryLandingContactSent',
            business_unit='FindASupplier',
            site_section='Industries',
            site_subsection='LandingContactSent'
        )

    @property
    def expected_referer_url(self):
        return reverse('sector-list-cms-contact')


class IndustryArticleCMSView(
    CMSLanguageSwitcherMixin, GetCMSPageMixin,
    CountryDisplayMixin, GA360Mixin, TemplateView
):
    template_name = 'industry/article.html'

    def __init__(self):
        super().__init__()

        self.set_ga360_payload(
            page_id='FindASupplierIndustryArticle',
            business_unit='FindASupplier',
            site_section='Industries',
            site_subsection='Article'
        )

    def get_context_data(self, *args, **kwargs):
        social_links_builder = SocialLinkBuilder(
            url=self.request.build_absolute_uri(),
            page_title=self.page['title'],
            app_title='Find A Supplier',
        )
        return super().get_context_data(
            page=self.page,
            social_links=social_links_builder.links,
            *args, **kwargs
        )


class IndustryLandingPageCMSView(
    CMSLanguageSwitcherMixin, ActiveViewNameMixin,
    CountryDisplayMixin, GA360Mixin, TemplateView
):
    active_view_name = 'sector-list'
    template_name = 'industry/list.html'

    def __init__(self):
        super().__init__()

        self.set_ga360_payload(
            page_id='FindASupplierIndustryLandingPage',
            business_unit='FindASupplier',
            site_section='Industries',
            site_subsection='LandingPage'
        )

    @cached_property
    def page(self):
        response = cms_api_client.lookup_by_slug(
            slug=slugs.FIND_A_SUPPLIER_INDUSTRY_LANDING,
            language_code=translation.get_language(),
            draft_token=self.request.GET.get('draft_token'),
        )
        return handle_cms_response(response)

    def get_context_data(self, *args, **kwargs):
        showcase_industries = self.get_showcase_industries(
            self.page['industries']
        )
        return super().get_context_data(
            page=self.page,
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
