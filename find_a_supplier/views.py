from directory_api_client.client import api_client
import directory_forms_api_client.helpers

from django.conf import settings
from django.core.paginator import EmptyPage, Paginator
from django.core.urlresolvers import reverse
from django.shortcuts import Http404, redirect
from django.template.response import TemplateResponse
from django.utils.functional import cached_property
from django.views.generic import RedirectView, TemplateView
from django.views.generic.edit import FormView
from directory_components.mixins import CountryDisplayMixin, GA360Mixin

from core.helpers import get_filters_labels, get_results_from_search_response
from find_a_supplier import forms, helpers
import core.mixins


class CompanyProfileMixin(core.mixins.CompanyProfileMixin):
    @cached_property
    def company(self):
        company = super().company
        if not company['is_published_find_a_supplier']:
            raise Http404(f'API returned 404 for company {company["number"]}')
        return company


class CompanySearchView(
    core.mixins.SubmitFormOnGetMixin,
    CountryDisplayMixin,
    core.mixins.PersistSearchQuerystringMixin,
    GA360Mixin,
    FormView
):
    template_name = 'find_a_supplier/search.html'
    form_class = forms.CompanySearchForm
    page_size = 10

    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id='FindASupplierCompanySearch',
            business_unit='FindASupplier',
            site_section='Companies',
            site_subsection='Search',
        )

    def dispatch(self, *args, **kwargs):
        if 'term' in self.request.GET:
            url = self.request.get_full_path()
            return redirect(url.replace('term=', 'q='))
        return super().dispatch(*args, **kwargs)

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
        response = api_client.company.search_company(
            term=form.cleaned_data['q'],
            page=form.cleaned_data['page'],
            sectors=form.cleaned_data['sectors'],
            size=self.page_size,
        )
        response.raise_for_status()
        formatted = get_results_from_search_response(response)
        return formatted['results'], formatted['hits']['total']

    @staticmethod
    def handle_empty_page(form):
        url = '{url}?q={q}'.format(
            url=reverse('find-a-supplier:search'),
            q=form.cleaned_data['q']
        )
        return redirect(url)

    @property
    def should_show_search_guide(self):
        """show the search guide if:

        - user explicitly asked for it; or
        - search was submitted with empty q or empty sectors; or
        - search was submitted with only empty q; or
        - search was submitted with only empty sectors

        """

        q = self.request.GET.get('q')
        sectors = self.request.GET.get('sectors')
        return any([
            'show-guide' in self.request.GET,
            q == '' and sectors == '',
            q == '' and sectors is None,
            sectors == '' and q is None,
        ])

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            show_search_guide=self.should_show_search_guide,
            **kwargs,
        )


class PublishedProfileListView(CountryDisplayMixin, GA360Mixin, RedirectView):

    def __init__(self):
        super().__init__()

        self.set_ga360_payload(
            page_id='FindASupplierPublishedProfileList',
            business_unit='FindASupplier',
            site_section='Companies',
            site_subsection='PublishedProfileList',
        )

    def get_redirect_url(self, *args, **kwargs):
        sectors = self.request.GET.get('sectors')
        if sectors:
            return '{url}?sector={sector}'.format(
                url=reverse('find-a-supplier:search'), sector=sectors
            )
        return reverse('find-a-supplier:search')


class ProfileView(
    CompanyProfileMixin,
    CountryDisplayMixin,
    GA360Mixin,
    core.mixins.PersistSearchQuerystringMixin,
    TemplateView,
):
    template_name = 'find_a_supplier/profile.html'

    def __init__(self):
        super().__init__()

        self.set_ga360_payload(
            page_id='FindASupplierPublishedProfileDetail',
            business_unit='FindASupplier',
            site_section='Companies',
            site_subsection='PublishedProfileDetail',
        )

    def get_canonical_url(self):
        kwargs = {
            'company_number': self.company['number'],
            'slug': self.company['slug'],
        }
        return reverse('find-a-supplier:profile', kwargs=kwargs)

    def get(self, *args, **kwargs):
        if self.kwargs.get('slug') != self.company['slug']:
            return redirect(to=self.get_canonical_url())
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
            social=social,
            **kwargs
        )


class CaseStudyDetailView(CountryDisplayMixin, GA360Mixin, TemplateView):
    template_name = 'find_a_supplier/supplier-case-study-detail.html'

    def __init__(self):
        super().__init__()

        self.set_ga360_payload(
            page_id='FindASupplierCaseStudyDetail',
            business_unit='FindASupplier',
            site_section='Companies',
            site_subsection='CaseStudy',
        )

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
            return redirect(to=self.get_canonical_url())
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


class ContactCompanyView(
    CompanyProfileMixin,
    CountryDisplayMixin,
    GA360Mixin,
    core.mixins.PersistSearchQuerystringMixin,
    FormView,
):
    template_name = 'find_a_supplier/contact.html'
    form_class = forms.ContactCompanyForm

    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id='FindASupplierContactCompany',
            business_unit='FindASupplier',
            site_section='Companies',
            site_subsection='ContactCompany',
        )

    def get_success_url(self):
        url = reverse(
            'find-a-supplier:company-contact-sent',
            kwargs={'company_number': self.kwargs['company_number']}
        )
        return f'{url}?{self.search_querystring}'

    def form_valid(self, form):
        response = self.send_email(form)
        response.raise_for_status()
        return super().form_valid(form)

    def send_email(self, form):
        sender = directory_forms_api_client.helpers.Sender(
            email_address=form.cleaned_data['email_address'],
            country_code=form.cleaned_data['country'],
        )
        spam_control = directory_forms_api_client.helpers.SpamControl(
            contents=[form.cleaned_data['subject'], form.cleaned_data['body']]
        )
        return form.save(
            template_id=settings.CONTACT_FAS_COMPANY_NOTIFY_TEMPLATE_ID,
            email_address=self.company['email_address'],
            form_url=self.request.path,
            sender=sender,
            spam_control=spam_control,
        )


class ContactCompanySentView(
    CompanyProfileMixin,
    GA360Mixin,
    core.mixins.PersistSearchQuerystringMixin,
    TemplateView
):

    template_name = 'find_a_supplier/sent.html'

    def __init__(self):
        super().__init__()

        self.set_ga360_payload(
            page_id='FindASupplierContactCompanySent',
            business_unit='FindASupplier',
            site_section='Companies',
            site_subsection='ContactCompanySent',
        )
