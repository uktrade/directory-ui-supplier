import http
import requests

from django.conf import settings
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.http import Http404

from api_client import api_client
from company import forms, helpers


class SubmitFormOnGetMixin:

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['data'] = self.request.GET or {}
        return kwargs

    def get(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class AddCompanyProfileToContextMixin:

    company_number_url_kwarg = 'company_number'

    def get_context_data(self, **kwargs):
        number = self.kwargs[self.company_number_url_kwarg]
        response = api_client.company.retrieve_public_profile(number=number)
        if response.status_code == http.client.NOT_FOUND:
            raise Http404(
                "API returned 404 for company number %s",
                self.kwargs['company_number'],
            )
        elif not response.ok:
            response.raise_for_status()
        company = helpers.get_public_company_profile_from_response(response)
        return super().get_context_data(company=company, **kwargs)


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
        if not response.ok:
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


class PublishedProfileDetailView(AddCompanyProfileToContextMixin,
                                 TemplateView):
    template_name = 'company-profile-detail.html'

    def get_context_data(self, **kwargs):
        is_verbose = 'verbose' in self.request.GET
        return super().get_context_data(show_description=is_verbose, **kwargs)


class CaseStudyDetailView(TemplateView):
    template_name = 'supplier-case-study-detail.html'

    def get_case_study(self):
        response = api_client.company.retrieve_public_case_study(
            case_study_id=self.kwargs['id'],
        )
        if response.status_code == http.client.NOT_FOUND:
            raise Http404(
                "API returned 404 for case study with id %s",
                self.kwargs['id'],
            )
        elif not response.ok:
            response.raise_for_status()
        return helpers.get_case_study_details_from_response(response)

    def get_context_data(self, **kwargs):
        return {
            'case_study': self.get_case_study(),
        }


class ContactCompanyView(AddCompanyProfileToContextMixin, FormView):
    template_name = 'company-contact-form.html'
    success_template_name = 'company-contact-success.html'
    failure_template_name = 'company-contact-error.html'
    form_class = forms.ContactCompanyForm

    def dispatch(self, *args, **kwargs):
        if not settings.FEATURE_CONTACT_COMPANY_FORM_ENABLED:
            raise Http404()
        return super().dispatch(*args, **kwargs)

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
