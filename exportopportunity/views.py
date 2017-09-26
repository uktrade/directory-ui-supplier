from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404
from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from directory_constants.constants import choices
from formtools.wizard.views import SessionWizardView

from api_client import api_client
from exportopportunity import forms, helpers
from ui.views import ConditionalEnableTranslationsMixin

FOOD_IS_GREAT = 'food-is-great'
industry_map = {
    FOOD_IS_GREAT: 'FOOD_AND_DRINK',
}


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


class SubmitExportOpportunityWizardView(
    LeadGenerationFeatureFlagMixin, ConditionalEnableTranslationsMixin,
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

    language_form_class = forms.LanguageLeadGeneartionForm

    def dispatch(self, *args, **kwargs):
        if (
            kwargs['campaign'] not in choices.LEAD_GENERATION_CAMPAIGNS or
            kwargs['country'] not in choices.LEAD_GENERATION_COUNTRIES
        ):
            raise Http404()
        return super().dispatch(*args, **kwargs)

    @property
    def translations_enabled(self):
        return (
            self.request.LANGUAGE_CODE not in
            settings.DISABLED_LANGUAGES_SUBMIT_OPPORTUNITY_PAGES
        )

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


class BaseCampaignView(
    LeadGenerationFeatureFlagMixin, ConditionalEnableTranslationsMixin,
    TemplateView
):
    template_name = None
    language_form_class = forms.LanguageCampaignForm

    @property
    def industry(self):
        return industry_map[self.kwargs['campaign']]

    @property
    def translations_enabled(self):
        return self.request.LANGUAGE_CODE in self.supported_languages

    def get_language_form_kwargs(self):
        return super().get_language_form_kwargs(
            language_codes=self.supported_languages
        )

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            case_studies=self.get_case_studies(),
            companies=self.get_showcase_companies(),
            lead_generation_url=self.get_lead_geneartion_url(),
            industry=self.industry,
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
        return helpers.get_showcase_case_studies(sector=self.industry)

    def get_showcase_companies(self):
        return helpers.get_showcase_companies(sector=self.industry,)


class FoodIsGreatCampaignView(BaseCampaignView):
    template_name = 'exportopportunity/campaign-food.html'

    @property
    def supported_languages(self):
        return settings.FOOD_IS_GREAT_ENABLED_LANGUAGES
