from urllib.parse import urlencode

from django.conf import settings
from django.core.paginator import EmptyPage, Paginator
from django.shortcuts import Http404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from directory_api_client.client import api_client
from directory_constants import expertise
from directory_components.mixins import CountryDisplayMixin, GA360Mixin

from core.views import BaseNotifyFormView
from core.helpers import (
    NotifySettings, get_filters_labels, get_results_from_search_response
)
import core.mixins
from investment_support_directory import forms, helpers


class CompanyProfileMixin(core.mixins.CompanyProfileMixin):
    @cached_property
    def company(self):
        company = super().company
        if not company['is_published_investment_support_directory']:
            raise Http404(f'API returned 404 for company {company["number"]}')
        return company


class HomeView(CountryDisplayMixin, GA360Mixin, FormView):
    template_name = 'investment_support_directory/home.html'
    form_class = forms.CompanyHomeSearchForm

    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id='FindASupplierISDHome',
            business_unit='FindASupplier',
            site_section='InvestmentSupportDirectory',
            site_subsection='Home'
        )

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            CHOICES_FINANCIAL=expertise.FINANCIAL,
            CHOICES_HUMAN_RESOURCES=expertise.HUMAN_RESOURCES,
            CHOICES_LEGAL=expertise.LEGAL,
            CHOICES_PUBLICITY=expertise.PUBLICITY,
            CHOICES_BUSINESS_SUPPORT=expertise.BUSINESS_SUPPORT,
            CHOICES_MANAGEMENT_CONSULTING=expertise.MANAGEMENT_CONSULTING,
            **kwargs,
        )

    def form_valid(self, form):
        url = reverse('investment-support-directory:search')
        return redirect(url + '?' + urlencode(self.request.POST))


class CompanySearchView(
    CountryDisplayMixin,
    core.mixins.SubmitFormOnGetMixin,
    core.mixins.PersistSearchQuerystringMixin,
    GA360Mixin,
    FormView,
):
    form_class = forms.CompanySearchForm
    page_size = 10
    template_name = 'investment_support_directory/search.html'

    def __init__(self):
        super().__init__()

        self.set_ga360_payload(
            page_id='FindASupplierISDCompanySearch',
            business_unit='FindASupplier',
            site_section='InvestmentSupportDirectory',
            site_subsection='CompanySearch'
        )

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            show_search_guide='show-guide' in self.request.GET,
            **kwargs,
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if 'data' not in kwargs:
            kwargs['data'] = {}
        return kwargs

    def form_valid(self, form):
        results, count = self.get_results_and_count(form)
        try:
            paginator = Paginator(range(count), self.page_size)
            pagination = paginator.page(form.cleaned_data['page'])
        except EmptyPage:
            return self.handle_empty_page(form)
        else:
            context = self.get_context_data(
                results=results,
                pagination=pagination,
                form=form,
                filters=get_filters_labels(form.cleaned_data),
                pages_after_current=paginator.num_pages - pagination.number,
                paginator_url=helpers.get_paginator_url(form.cleaned_data)
            )
            return TemplateResponse(self.request, self.template_name, context)

    def get_results_and_count(self, form):
        if 'show-guide' in self.request.GET:
            return [], 0
        data = form.cleaned_data
        response = api_client.company.search_investment_search_directory(
            term=data['q'],
            page=data['page'],
            size=self.page_size,
            expertise_industries=data.get('expertise_industries'),
            expertise_regions=data.get('expertise_regions'),
            expertise_countries=data.get('expertise_countries'),
            expertise_languages=data.get('expertise_languages'),
            expertise_financial=data.get('expertise_financial'),
            expertise_products_services_labels=(
                data.get('expertise_products_services_labels')
            )
        )
        response.raise_for_status()
        formatted = get_results_from_search_response(response)
        return formatted['results'], formatted['hits']['total']

    @staticmethod
    def handle_empty_page(form):
        # get_paginator_url returns urls wih all active filters except `page`
        return redirect(helpers.get_paginator_url(form.cleaned_data))


class ProfileView(
    CompanyProfileMixin,
    CountryDisplayMixin,
    core.mixins.PersistSearchQuerystringMixin,
    GA360Mixin,
    TemplateView
):
    template_name = 'investment_support_directory/profile.html'

    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id='FindASupplierISDProfile',
            business_unit='FindASupplier',
            site_section='InvestmentSupportDirectory',
            site_subsection='Profile'
        )

    def get_canonical_url(self):
        kwargs = {
            'company_number': self.company['number'],
            'slug': self.company['slug'],
        }
        return reverse('investment-support-directory:profile', kwargs=kwargs)

    def get(self, *args, **kwargs):
        if self.kwargs.get('slug') != self.company['slug']:
            return redirect(to=self.get_canonical_url())
        return super().get(*args, **kwargs)


class ContactView(
    CompanyProfileMixin,
    CountryDisplayMixin,
    core.mixins.PersistSearchQuerystringMixin,
    GA360Mixin,
    BaseNotifyFormView,
):

    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id='FindASupplierISDContact',
            business_unit='FindASupplier',
            site_section='InvestmentSupportDirectory',
            site_subsection='Contact'
        )

    form_class = forms.ContactCompanyForm
    template_name = 'investment_support_directory/contact.html'
    notify_settings = NotifySettings(
        company_template=settings.CONTACT_ISD_COMPANY_NOTIFY_TEMPLATE_ID,
        support_template=settings.CONTACT_ISD_SUPPORT_NOTIFY_TEMPLATE_ID,
        support_email_address=settings.CONTACT_ISD_SUPPORT_EMAIL_ADDRESS,
        investor_template=settings.CONTACT_ISD_INVESTOR_NOTIFY_TEMPLATE_ID,
    )

    def get_success_url(self):
        url = reverse(
            'investment-support-directory:company-contact-sent',
            kwargs={'company_number': self.kwargs['company_number']}
        )
        return f'{url}?{self.search_querystring}'


class ContactSuccessView(
    CompanyProfileMixin,
    CountryDisplayMixin,
    core.mixins.PersistSearchQuerystringMixin,
    GA360Mixin,
    TemplateView
):
    template_name = 'investment_support_directory/sent.html'

    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id='FindASupplierISDContactSuccess',
            business_unit='FindASupplier',
            site_section='InvestmentSupportDirectory',
            site_subsection='ContactSuccess'
        )
