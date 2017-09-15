from django.conf import settings
from django.http import Http404
from django.template.response import TemplateResponse
from django.views.generic.edit import FormView
from django.views.generic import TemplateView

from api_client import api_client
from exportopportunity import forms


class LeadGenerationFeatureFlagMixin:
    def dispatch(self, request, *args, **kwargs):
        if not settings.FEATURE_EXPORT_OPPORTUNITY_LEAD_GENERATION_ENABLED:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)


class SubmitExportOpportunityView(LeadGenerationFeatureFlagMixin, FormView):
    form_class = forms.OpportunityForm
    template_name = 'export-opportunity.html'
    success_template = 'export-opportunity-success.html'

    def form_valid(self, form):
        response = api_client.exportopportunity.create_opportunity(
            form_data=form.cleaned_data
        )
        response.raise_for_status()
        return TemplateResponse(self.request, self.success_template)


class LeadGenerationFoodView(LeadGenerationFeatureFlagMixin, TemplateView):
    template_name = 'lead_generation/food.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            case_studies=self.get_case_studies(),
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
