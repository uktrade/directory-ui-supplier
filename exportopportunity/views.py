from django.conf import settings
from django.http import Http404
from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from formtools.wizard.views import SessionWizardView

from api_client import api_client
from exportopportunity import forms


class LeadGenerationFeatureFlagMixin:
    def dispatch(self, request, *args, **kwargs):
        if not settings.FEATURE_EXPORT_OPPORTUNITY_LEAD_GENERATION_ENABLED:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)


class GetTemplateForCurrentStepMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert self.templates

    def get_template_names(self):
        return [self.templates[self.steps.current]]


class SubmitExportOpportunityView(
    LeadGenerationFeatureFlagMixin, GetTemplateForCurrentStepMixin,
    SessionWizardView
):
    SECTOR = 'sector'
    NEEDS = 'needs'
    CONTACT = 'contact'
    SUCCESS = 'success'

    form_list = (
        (SECTOR, forms.OpportunityBusinessSectorForm),
        (NEEDS, forms.OpportunityNeedForm),
        (CONTACT, forms.OpportunityContactDetailsForm),
    )
    templates = {
        SECTOR: 'export-opportunity-sector.html',
        NEEDS: 'export-opportunity-needs.html',
        CONTACT: 'export-opportunity-contact.html',
        SUCCESS: 'export-opportunity-success.html',
    }

    def done(self, form):
        response = api_client.exportopportunity.create_opportunity(
            form_data=self.get_all_cleaned_data(),
        )
        response.raise_for_status()
        return TemplateResponse(self.request, self.templates[self.SUCCESS])


class LeadGenerationFoodView(LeadGenerationFeatureFlagMixin, TemplateView):
    template_name = 'lead_generation/food.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            case_studies=self.get_case_studies(),
            companies=self.get_companies(),
            **kwargs
        )

    def get_case_studies(self):
        return [
            {
                'image_url': 'https://unsplash.it/900?random',
                'case_study_url': 'http://www.google.com',
                'name': 'Company 1',
            },
            {
                'image_url': 'https://unsplash.it/800?random',
                'case_study_url': 'http://www.google.com',
                'name': 'Company 2',
            },
            {
                'image_url': 'https://unsplash.it/700?random',
                'case_study_url': 'http://www.google.com',
                'name': 'Company 3',
            },
        ]

    def get_companies(self):
        return [
            {
                'name': 'Good Company',
                'incorporation_year': '1998',
                'number_of_employees': '100 to 200',
                'profile_url': 'http://www.google.com',
                'logo': 'https://unsplash.it/901?random',
            },
            {
                'name': 'Bad Company',
                'incorporation_year': '2001',
                'number_of_employees': '100 to 200',
                'profile_url': 'http://www.google.com',
                'logo': 'https://unsplash.it/902?random',
            },
            {
                'name': 'Abhorrent Company',
                'incorporation_year': '1995',
                'number_of_employees': '100 to 200',
                'profile_url': 'http://www.google.com',
                'logo': 'https://unsplash.it/903?random',
            },
        ]
