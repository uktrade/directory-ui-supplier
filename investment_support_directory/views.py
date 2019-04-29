from urllib.parse import urlencode

from directory_api_client.client import api_client
from directory_components.mixins import CountryDisplayMixin

from django.conf import settings
from django.core.paginator import EmptyPage, Paginator
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

import core.mixins
from investment_support_directory import forms, helpers


class FeatureFlagMixin(core.mixins.NotFoundOnDisabledFeature):

    @property
    def flag(self):
        return settings.FEATURE_FLAGS['INVESTMENT_SUPPORT_DIRECTORY_ON']


class HomeView(FeatureFlagMixin, CountryDisplayMixin, FormView):
    template_name = 'investment_support_directory/home.html'
    form_class = forms.CompanyHomeSearchForm

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            CHOICES_FINANCIAL=forms.CHOICES_FINANCIAL,
            CHOICES_HUMAN_RESOURCES=forms.CHOICES_HUMAN_RESOURCES,
            CHOICES_LEGAL=forms.CHOICES_LEGAL,
            CHOICES_PUBLICITY=forms.CHOICES_PUBLICITY,
            CHOICES_FURTHER_SERVICES=forms.CHOICES_FURTHER_SERVICES,
            CHOICES_MANAGEMENT_CONSULTING=forms.CHOICES_MANAGEMENT_CONSULTING,
            **kwargs,
        )

    def form_valid(self, form):
        url = reverse('investment-support-directory-search')
        return redirect(url + '?' + urlencode(self.request.POST))


class CompanySearchView(
    FeatureFlagMixin, CountryDisplayMixin, core.mixins.SubmitFormOnGetMixin,
    FormView
):
    form_class = forms.CompanySearchForm
    page_size = 10
    template_name = 'investment_support_directory/search.html'

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
                filters=helpers.get_filters_labels(form.cleaned_data),
                pages_after_current=paginator.num_pages - pagination.number,
                paginator_url=helpers.get_paginator_url(form.cleaned_data)
            )
            return TemplateResponse(self.request, self.template_name, context)

    def get_results_and_count(self, form):
        data = form.cleaned_data
        response = api_client.company.search_investment_search_directory(
            term=data['term'],
            page=data['page'],
            size=self.page_size,
            expertise_industries=data.get('expertise_industries'),
            expertise_regions=data.get('expertise_regions'),
            expertise_countries=data.get('expertise_countries'),
            expertise_languages=data.get('expertise_languages'),
            expertise_financial=data.get('expertise_financial'),
            expertise_products_services=data.get('expertise_products_services')
        )
        response.raise_for_status()
        formatted = helpers.get_results_from_search_response(response)
        return formatted['results'], formatted['hits']['total']

    @staticmethod
    def handle_empty_page(form):
        url = '{url}?term={term}'.format(
            url=reverse('investment-support-directory-search'),
            term=form.cleaned_data['term']
        )
        return redirect(url)


class ProfileView(FeatureFlagMixin, CountryDisplayMixin, TemplateView):
    template_name = 'investment_support_directory/profile.html'

    def get_canonical_url(self):
        kwargs = {
            'company_number': self.company['number'],
            'slug': self.company['slug'],
        }
        return reverse('investment-support-directory-profile', kwargs=kwargs)

    def get(self, *args, **kwargs):
        if self.kwargs.get('slug') != self.company['slug']:
            return redirect(to=self.get_canonical_url())
        return super().get(*args, **kwargs)

    @cached_property
    def company(self):
        return helpers.get_company_profile(self.kwargs['company_number'])

    def get_context_data(self, **kwargs):
        company = helpers.CompanyParser(self.company)
        return super().get_context_data(
            company=company.serialize_for_template(),
            **kwargs
        )
