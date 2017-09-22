from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404
from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from formtools.wizard.views import SessionWizardView

from api_client import api_client
from exportopportunity import forms, helpers

FOOD_IS_GREAT = 'food-is-great'
industry_map = {
    FOOD_IS_GREAT: 'FOOD_AND_DRINK',
}


class LeadGenerationFeatureFlagMixin:
    def dispatch(self, request, *args, **kwargs):
        if not settings.FEATURE_EXPORT_OPPORTUNITY_LEAD_GENERATION_ENABLED:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)


class WhitelistCampaignMixin:
    def dispatch(self, *args, **kwargs):
        if kwargs['campaign'] not in industry_map:
            raise Http404()
        return super().dispatch(*args, **kwargs)


class GetTemplateForCurrentStepMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert self.templates

    def get_template_names(self):
        return [self.templates[self.steps.current]]


class SubmitExportOpportunityWizardView(
    LeadGenerationFeatureFlagMixin, WhitelistCampaignMixin,
    GetTemplateForCurrentStepMixin, SessionWizardView
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
        SECTOR: 'exportopportunity/lead-generation-form-sector.html',
        NEEDS: 'exportopportunity/lead-generation-form-needs.html',
        CONTACT: 'exportopportunity/lead-generation-form-contact.html',
    }

    success_template_map = {
        FOOD_IS_GREAT:  'exportopportunity/lead-generation-success-food.html',
    }

    def done(self, *args, **kwargs):
        form_data = {
            'campaign': self.kwargs['campaign'],
            'country': self.kwargs['country'],
            **self.get_all_cleaned_data(),
        }
        response = api_client.exportopportunity.create_opportunity(
            form_data=form_data
        )
        response.raise_for_status()
        return TemplateResponse(
            self.request,
            self.success_template_map[self.kwargs['campaign']],
            {
                'industry': industry_map[self.kwargs['campaign']],
                'companies': self.get_showcase_companies(),
            }
        )

    def get_showcase_companies(self):
        return helpers.get_showcase_companies(
            sector=industry_map[self.kwargs['campaign']],
        )


class CampaignView(
    LeadGenerationFeatureFlagMixin, WhitelistCampaignMixin, TemplateView
):

    template_map = {
        FOOD_IS_GREAT:  'exportopportunity/campaign-food.html',
    }

    def get_template_names(self):
        return [self.template_map[self.kwargs['campaign']]]

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            case_studies=self.get_case_studies(),
            companies=self.get_showcase_companies(),
            lead_generation_url=self.get_lead_geneartion_url(),
            industry=industry_map[self.kwargs['campaign']],
            **kwargs
        )

    def get_lead_geneartion_url(self):
        return reverse(
            'lead-generation-submit',
            kwargs={
                'campaign': self.kwargs['campaign'],
                'country': self.kwargs['country'],
            }
        )

    def get_case_studies(self):
        return helpers.get_showcase_case_studies(
            sector=industry_map[self.kwargs['campaign']],
        )

    def get_showcase_companies(self):
        return helpers.get_showcase_companies(
            sector=industry_map[self.kwargs['campaign']],
        )
