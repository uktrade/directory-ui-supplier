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
