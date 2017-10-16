from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404
from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from directory_constants.constants import lead_generation, sectors
from formtools.wizard.views import SessionWizardView

from api_client import api_client
from exportopportunity import forms, helpers
from ui.views import ConditionalEnableTranslationsMixin


industry_map = {
    lead_generation.FOOD_IS_GREAT: sectors.FOOD_AND_DRINK,
    lead_generation.LEGAL_IS_GREAT: 'LEGAL',
}


class GetTemplateForCurrentStepMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert self.templates

    def get_template_names(self):
        return [self.templates[self.steps.current]]


class GetShowcaseResourcesMixin:
    query_showcase_resources_by_campaign_tag = False
    industry = None
    campaign_tag = None

    def get_case_studies(self):
        return helpers.get_showcase_case_studies(**self.get_showcase_query())

    def get_showcase_companies(self):
        return helpers.get_showcase_companies(**self.get_showcase_query())

    def get_showcase_query(self):
        if self.query_showcase_resources_by_campaign_tag:
            return {'campaign_tag': self.campaign_tag}
        else:
            return {'sectors': industry_map[self.kwargs['campaign']]}


class BaseOpportunityWizardView(
    ConditionalEnableTranslationsMixin, GetShowcaseResourcesMixin,
    GetTemplateForCurrentStepMixin, SessionWizardView
):
    SECTOR = 'sector'
    NEEDS = 'needs'
    CONTACT = 'contact'
    SUCCESS = 'success'

    templates = {
        SECTOR: 'exportopportunity/lead-generation-form-sector.html',
        NEEDS: 'exportopportunity/lead-generation-form-needs.html',
        CONTACT: 'exportopportunity/lead-generation-form-contact.html',
    }

    success_template_map = {
        lead_generation.FOOD_IS_GREAT: (
            'exportopportunity/lead-generation-success-food.html'
        ),
        lead_generation.LEGAL_IS_GREAT: (
            'exportopportunity/lead-generation-success-legal.html'
        ),
    }

    language_form_class = forms.LanguageLeadGeneartionForm

    should_skip_captcha = False

    def dispatch(self, *args, **kwargs):
        if not settings.FEATURE_EXPORT_OPPORTUNITY_LEAD_GENERATION_ENABLED:
            raise Http404()
        return super().dispatch(*args, **kwargs)

    @property
    def translations_enabled(self):
        return (
            self.request.LANGUAGE_CODE not in
            settings.DISABLED_LANGUAGES_SUBMIT_OPPORTUNITY_PAGES
        )

    @property
    def opportunity_create_handler(self):
        if self.kwargs['campaign'] == lead_generation.FOOD_IS_GREAT:
            return api_client.exportopportunity.create_opportunity_food
        elif self.kwargs['campaign'] == lead_generation.LEGAL_IS_GREAT:
            return api_client.exportopportunity.create_opportunity_legal

    def done(self, *args, **kwargs):
        form_data = {
            'campaign': self.kwargs['campaign'],
            'country': self.kwargs['country'],
            **self.get_all_cleaned_data(),
        }
        response = self.opportunity_create_handler(form_data=form_data)
        response.raise_for_status()
        return TemplateResponse(
            self.request,
            self.success_template_map[self.kwargs['campaign']],
            {
                'industry': industry_map[self.kwargs['campaign']],
                'companies': self.get_showcase_companies(),
            }
        )

    def render_done(self, *args, **kwargs):
        # django-forms runs form.is_valid() for all steps after the final step
        # meaning the same captcha code is sent to google multiple times.
        # Google rejects the code the second time as it's already seen it and
        # thinks the second is a "replay attack" - so prevent formtools from
        # validating the captcha twice.
        self.should_skip_captcha = True
        return super().render_done(*args, **kwargs)

    def get_form_kwargs(self, step):
        kwargs = super().get_form_kwargs(step=step)
        if step == self.CONTACT and self.should_skip_captcha:
            kwargs['skip_captcha_errors'] = True
        return kwargs


class FoodIsGreatOpportunityWizardView(BaseOpportunityWizardView):
    form_list = (
        (
            BaseOpportunityWizardView.SECTOR,
            forms.OpportunityBusinessSectorFoodForm
        ),
        (
            BaseOpportunityWizardView.NEEDS,
            forms.OpportunityNeedFoodForm
        ),
        (
            BaseOpportunityWizardView.CONTACT,
            forms.OpportunityContactDetailsForm
        ),
    )


class LegalIsGreatOpportunityWizardView(BaseOpportunityWizardView):
    campaign_tag = lead_generation.LEGAL_IS_GREAT
    query_showcase_resources_by_campaign_tag = True
    form_list = (
        (
            BaseOpportunityWizardView.SECTOR,
            forms.OpportunityBusinessSectorLegalForm
        ),
        (
            BaseOpportunityWizardView.NEEDS,
            forms.OpportunityNeedLegalForm
        ),
        (
            BaseOpportunityWizardView.CONTACT,
            forms.OpportunityContactDetailsForm
        ),
    )


class BaseCampaignView(
    ConditionalEnableTranslationsMixin, GetShowcaseResourcesMixin, TemplateView
):
    template_name = None
    language_form_class = forms.LanguageCampaignForm
    feature_flag = None
    search_keyword = None

    @property
    def translations_enabled(self):
        return self.request.LANGUAGE_CODE in self.supported_languages

    def dispatch(self, *args, **kwargs):
        if not self.feature_flag:
            raise Http404()
        return super().dispatch(*args, **kwargs)

    def get_language_form_kwargs(self):
        return super().get_language_form_kwargs(
            language_codes=self.supported_languages
        )

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            case_studies=self.get_case_studies(),
            companies=self.get_showcase_companies(),
            lead_generation_url=self.get_lead_geneartion_url(),
            industry=industry_map[self.kwargs['campaign']],
            is_lead_generation_enabled=self.is_lead_generation_enabled,
            search_keyword=self.search_keyword,
            **kwargs,
        )

    def get_lead_geneartion_url(self):
        campaign_map = {
            (lead_generation.FOOD_IS_GREAT, lead_generation.FRANCE):
                'food-is-great-lead-generation-submit-france',
            (lead_generation.LEGAL_IS_GREAT, lead_generation.FRANCE):
                'legal-is-great-lead-generation-submit-france',
            (lead_generation.FOOD_IS_GREAT, lead_generation.SINGAPORE):
                'food-is-great-lead-generation-submit-singapore',
            (lead_generation.LEGAL_IS_GREAT, lead_generation.SINGAPORE):
                'legal-is-great-lead-generation-submit-singapore',
        }
        name = campaign_map[(self.kwargs['campaign'], self.kwargs['country'])]
        return reverse(name)

    @property
    def is_lead_generation_enabled(self):
        return self.kwargs['country'] not in self.disabled_countries


class FoodIsGreatCampaignView(BaseCampaignView):
    template_name = 'exportopportunity/campaign-food.html'

    @property
    def feature_flag(self):
        return settings.FEATURE_FOOD_CAMPAIGN_ENABLED

    @property
    def supported_languages(self):
        return settings.FOOD_IS_GREAT_ENABLED_LANGUAGES

    @property
    def disabled_countries(self):
        return settings.FOOD_CAMPAIGN_DISABLED_COUNTRIES

    @property
    def search_keyword(self):
        return settings.FOOD_IS_GREAT_SEARCH_KEYWORD


class LegalIsGreatCampaignView(BaseCampaignView):
    template_name = 'exportopportunity/campaign-legal.html'
    query_showcase_resources_by_campaign_tag = True
    campaign_tag = lead_generation.LEGAL_IS_GREAT

    @property
    def feature_flag(self):
        return settings.FEATURE_LEGAL_CAMPAIGN_ENABLED

    @property
    def supported_languages(self):
        return settings.LEGAL_IS_GREAT_ENABLED_LANGUAGES

    @property
    def disabled_countries(self):
        return settings.LEGAL_CAMPAIGN_DISABLED_COUNTRIES

    @property
    def search_keyword(self):
        return settings.LEGAL_IS_GREAT_SEARCH_KEYWORD
