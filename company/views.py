from directory_api_client.client import api_client
import directory_forms_api_client.helpers

from django.conf import settings
from django.core.paginator import EmptyPage, Paginator
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.functional import cached_property
from django.views.generic import RedirectView, TemplateView
from django.views.generic.edit import FormView
from directory_components.mixins import CountryDisplayMixin, GA360Mixin

from company import forms, helpers
import core.mixins


class CompanyProfileMixin:

    @cached_property
    def company(self):
        return helpers.get_company_profile(self.kwargs['company_number'])


class CompanySearchView(
    core.mixins.SubmitFormOnGetMixin, CountryDisplayMixin, GA360Mixin, FormView
):
    template_name = 'company-search-results-list.html'
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
                form=form,
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
        formatted = helpers.get_results_from_search_response(response)
        return formatted['results'], formatted['hits']['total']

    @staticmethod
    def handle_empty_page(form):
        url = '{url}?q={q}'.format(
            url=reverse('company-search'),
            q=form.cleaned_data['q']
        )
        return redirect(url)


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
                url=reverse('company-search'), sector=sectors
            )
        return reverse('company-search')


class PublishedProfileDetailView(
    CompanyProfileMixin, CountryDisplayMixin, GA360Mixin, TemplateView
):
    template_name = 'company-profile-detail.html'

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
        return reverse('public-company-profiles-detail', kwargs=kwargs)

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
            company=self.company,
            **kwargs
        )


class CaseStudyDetailView(CountryDisplayMixin, GA360Mixin, TemplateView):
    template_name = 'supplier-case-study-detail.html'

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


class ContactCompanyView(CompanyProfileMixin,
                         CountryDisplayMixin,
                         GA360Mixin,
                         FormView):
    template_name = 'company-contact-form.html'
    form_class = forms.ContactCompanyForm

    def __init__(self):
        super().__init__()

        self.set_ga360_payload(
            page_id='FindASupplierContactCompany',
            business_unit='FindASupplier',
            site_section='Companies',
            site_subsection='ContactCompany',
        )

    def get_context_data(self, **kwargs):
        return super().get_context_data(company=self.company, **kwargs)

    def get_success_url(self):
        return reverse(
            'contact-company-sent',
            kwargs={'company_number': self.kwargs['company_number']}
        )

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
            recipients=[self.company['email_address']],
            subject=settings.CONTACT_SUPPLIER_SUBJECT,
            reply_to=[form.cleaned_data['email_address']],
            recipient_name=self.company['name'],
            form_url=self.request.path,
            sender=sender,
            spam_control=spam_control,
        )


class ContactCompanySentView(CompanyProfileMixin, GA360Mixin, TemplateView):

    template_name = 'company-contact-success.html'

    def __init__(self):
        super().__init__()

        self.set_ga360_payload(
            page_id='FindASupplierContactCompanySent',
            business_unit='FindASupplier',
            site_section='Companies',
            site_subsection='ContactCompanySent',
        )

    def get_context_data(self, **kwargs):
        return super().get_context_data(company=self.company, **kwargs)
