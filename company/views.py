import http

import requests

from django.conf import settings
from django.core.paginator import EmptyPage, Paginator
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.functional import cached_property
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from api_client import api_client
from company import forms, helpers


class SubmitFormOnGetMixin:

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['data'] = self.request.GET or {}
        return kwargs

    def get(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CompanySearchView(SubmitFormOnGetMixin, FormView):
    template_name = 'company-search-results-list.html'
    form_class = forms.CompanySearchForm
    page_size = 10

    def dispatch(self, *args, **kwargs):
        if not settings.FEATURE_COMPANY_SEARCH_VIEW_ENABLED:
            raise Http404()
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            active_view_name='public-company-profiles-list',
            **kwargs,
        )

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
            )
            return TemplateResponse(self.request, self.template_name, context)

    def get_results_and_count(self, form):
        response = api_client.company.search(
            term=form.cleaned_data['term'],
            page=form.cleaned_data['page']-1,  # ElasticSearch is 0-indexed
            size=self.page_size,
        )
        response.raise_for_status()
        formatted = helpers.get_results_from_search_response(response)
        return formatted['results'], formatted['hits']['total']

    @staticmethod
    def handle_empty_page(form):
        url = '{url}?term={term}'.format(
            url=reverse('company-search'),
            sector=form.cleaned_data['term']
        )
        return redirect(url)


class PublishedProfileListView(SubmitFormOnGetMixin, FormView):
    template_name = 'company-public-profile-list.html'
    form_class = forms.PublicProfileSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_sector_label'] = self.get_sector_label(context)
        context['show_companies_count'] = self.get_show_companies_count()
        context['active_view_name'] = 'public-company-profiles-list'
        return context

    def get_show_companies_count(self):
        return bool(self.request.GET.get('sectors'))

    def get_sector_label(self, context):
        form = context['form']
        if form.is_valid():
            return helpers.get_sectors_label(form.cleaned_data['sectors'])
        return ''

    def get_results_and_count(self, form):
        response = api_client.company.list_public_profiles(
            sectors=form.cleaned_data['sectors'],
            page=form.cleaned_data['page']
        )
        response.raise_for_status()
        formatted = helpers.get_company_list_from_response(response)
        return formatted['results'], formatted['count']

    def handle_empty_page(self, form):
        url = '{url}?sectors={sector}'.format(
            url=reverse('public-company-profiles-list'),
            sector=form.cleaned_data['sectors']
        )
        return redirect(url)

    def form_valid(self, form):
        try:
            results, count = self.get_results_and_count(form)
        except requests.exceptions.HTTPError as error:
            if error.response.status_code == http.client.NOT_FOUND:
                # supplier entered a page number returning no results, so
                # redirect them back to the first page
                return self.handle_empty_page(form)
            raise
        else:
            context = self.get_context_data()
            paginator = Paginator(range(count), 10)
            context['pagination'] = paginator.page(form.cleaned_data['page'])
            context['companies'] = results
            return TemplateResponse(self.request, self.template_name, context)


class PublishedProfileDetailView(TemplateView):
    template_name = 'company-profile-detail.html'

    @cached_property
    def company(self):
        return helpers.get_company_profile(self.kwargs['company_number'])

    def get_canonical_url(self):
        kwargs = {
            'company_number': self.company['number'],
            'slug': self.company['slug'],
        }
        return reverse('public-company-profiles-detail', kwargs=kwargs)

    def get(self, *args, **kwargs):
        if self.kwargs.get('slug') != self.company['slug']:
            return redirect(to=self.get_canonical_url(), permanent=True)
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        social = {
            'title': (
                'International trade profile: {0}'.format(self.company['name'])
            ),
            'description': self.company['summary'],
            'image': self.company['logo'],
        }
        return super().get_context_data(
            show_description='verbose' in self.request.GET,
            company=self.company,
            social=social,
            **kwargs
        )


class CaseStudyDetailView(TemplateView):
    template_name = 'supplier-case-study-detail.html'

    @cached_property
    def case_study(self):
        return helpers.get_case_study(self.kwargs['id'])

    def get_canonical_url(self):
        kwargs = {
            'id': self.case_study['pk'],
            'slug': self.case_study['slug'],
        }
        return reverse('case-study-details', kwargs=kwargs)

    def get(self, *args, **kwargs):
        if self.kwargs.get('slug') != self.case_study['slug']:
            return redirect(to=self.get_canonical_url(), permanent=True)
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        social = {
            'title': 'Project: {title}'.format(title=self.case_study['title']),
            'description': self.case_study['description'],
            'image': self.case_study['image_one'],
        }
        return super().get_context_data(
            case_study=self.case_study,
            social=social,
            **kwargs
        )


class ContactCompanyView(FormView):
    template_name = 'company-contact-form.html'
    success_template_name = 'company-contact-success.html'
    failure_template_name = 'company-contact-error.html'
    form_class = forms.ContactCompanyForm

    def form_valid(self, form):
        data = self.serialize_form_data(
            cleaned_data=form.cleaned_data,
            company_number=self.kwargs['company_number'],
        )
        response = api_client.company.send_email(data)
        if response.ok:
            template = self.success_template_name
        else:
            template = self.failure_template_name
        context = self.get_context_data()
        return TemplateResponse(self.request, template, context)

    @staticmethod
    def serialize_form_data(cleaned_data, company_number):
        return forms.serialize_contact_company_form(
            cleaned_data,
            company_number,
        )

    def get_context_data(self, **kwargs):
        company = helpers.get_company_profile(self.kwargs['company_number'])
        return super().get_context_data(company=company, **kwargs)
