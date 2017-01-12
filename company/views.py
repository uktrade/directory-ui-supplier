import http
import requests

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
        kwargs['data'] = self.request.GET or None
        return kwargs

    def get(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PublicProfileListView(SubmitFormOnGetMixin, FormView):
    template_name = 'company-public-profile-list.html'
    form_class = forms.PublicProfileSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context['form']
        if form.is_valid():
            sector = helpers.get_sectors_label(form.cleaned_data['sectors'])
            context['selected_sector_label'] = sector
        return context

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


class PublicProfileDetailView(TemplateView):
    template_name = 'company-profile-detail.html'

    def get_context_data(self, **kwargs):
        api_call = (
            api_client.company.
            retrieve_public_profile_by_companies_house_number
        )
        response = api_call(number=self.kwargs['company_number'])
        if response.status_code == http.client.NOT_FOUND:
            raise Http404(
                "API returned 404 for company number %s",
                self.kwargs['company_number'],
            )
        elif not response.ok:
            response.raise_for_status()
        company = helpers.get_public_company_profile_from_response(response)
        return {
            'company': company,
            'show_edit_links': False,
        }


class CaseStudyDetailView(TemplateView):
    template_name = 'supplier-case-study-detail.html'

    def get_case_study(self):
        response = api_client.company.retrieve_public_case_study(
            case_study_id=self.kwargs['id'],
        )
        if not response.ok:
            response.raise_for_status()
        return helpers.get_case_study_details_from_response(response)

    def get_context_data(self, **kwargs):
        return {
            'case_study': self.get_case_study(),
        }
