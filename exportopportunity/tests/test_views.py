from unittest.mock import call, patch, Mock

from directory_constants.constants import lead_generation
import pytest

from django.core.urlresolvers import reverse

from exportopportunity import views


showcase_companies = [{'name': 'Showcase company 1'}]
showcase_case_studies = [{'name': 'Case study 1'}]


@pytest.fixture
def showcase_objects():
    patch_one = patch.object(
        views.helpers, 'get_showcase_companies',
        return_value=showcase_companies
    )
    patch_two = patch.object(
        views.helpers, 'get_showcase_case_studies',
        return_value=showcase_case_studies
    )
    patch_one.start()
    patch_two.start()
    yield
    patch_one.stop()
    patch_two.stop()


@pytest.mark.parametrize('enabled,status', ((False, 404), (True, 200)))
def test_lead_generation_feature_flag(enabled, status, client, settings):
    settings.FEATURE_EXPORT_OPPORTUNITY_LEAD_GENERATION_ENABLED = enabled
    url = reverse(
        'lead-generation-submit',
        kwargs={
            'campaign': lead_generation.FOOD_IS_GREAT,
            'country': lead_generation.FRANCE
        }
    )
    response = client.get(url)

    assert response.status_code == status


@pytest.mark.parametrize('url,enabled,status', (
    (reverse('food-is-great-campaign-france'),    True,  200),
    (reverse('food-is-great-campaign-singapore'), True,  200),
    (reverse('food-is-great-campaign-france'),    False, 404),
    (reverse('food-is-great-campaign-singapore'), False, 404),
))
@patch.object(views.helpers, 'get_showcase_companies',
              Mock(return_value=showcase_companies))
@patch.object(views.helpers, 'get_showcase_case_studies',
              Mock(return_value=showcase_case_studies))
def test_food_is_great_feature_flag(url, enabled, status, client, settings):
    settings.FEATURE_FOOD_CAMPAIGN_ENABLED = enabled

    response = client.get(url)

    assert response.status_code == status


@pytest.mark.parametrize('url,enabled,status', (
    (reverse('legal-is-great-campaign-france'),    True,  200),
    (reverse('legal-is-great-campaign-singapore'), True,  200),
    (reverse('legal-is-great-campaign-france'),    False, 404),
    (reverse('legal-is-great-campaign-singapore'), False, 404),
))
@patch.object(views.helpers, 'get_showcase_companies',
              Mock(return_value=showcase_companies))
@patch.object(views.helpers, 'get_showcase_case_studies',
              Mock(return_value=showcase_case_studies))
def test_legal_is_great_feature_flag(url, enabled, status, client, settings):
    settings.FEATURE_LEGAL_CAMPAIGN_ENABLED = enabled

    response = client.get(url)

    assert response.status_code == status


@pytest.mark.parametrize('url,sector,template_name', (
    (
        reverse('food-is-great-campaign-france'),
        'FOOD_AND_DRINK',
        'exportopportunity/campaign-food.html'
    ),
    (
        reverse('food-is-great-campaign-singapore'),
        'FOOD_AND_DRINK',
        'exportopportunity/campaign-food.html'
    ),
    (
        reverse('legal-is-great-campaign-france'),
        'LEGAL_SERVICES',
        'exportopportunity/campaign-legal.html'
    ),
    (
        reverse('legal-is-great-campaign-singapore'),
        'LEGAL_SERVICES',
        'exportopportunity/campaign-legal.html'
    ),
))
@patch.object(views.helpers, 'get_showcase_companies',
              return_value=showcase_companies)
@patch.object(views.helpers, 'get_showcase_case_studies',
              return_value=showcase_case_studies)
def test_exportopportunity_view_context(
    mock_get_showcase_case_studies, mock_get_showcase_companies, url, sector,
    template_name, client, settings
):
    settings.FEATURE_EXPORT_OPPORTUNITY_LEAD_GENERATION_ENABLED = True

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [template_name]
    assert response.context['industry'] == sector
    assert response.context['companies'] == showcase_companies
    assert response.context['case_studies'] == showcase_case_studies
    assert mock_get_showcase_companies.call_count == 1
    assert mock_get_showcase_companies.call_args == call(sector=sector)
    assert mock_get_showcase_case_studies.call_count == 1
    assert mock_get_showcase_case_studies.call_args == call(sector=sector)


@pytest.mark.parametrize('campaign,country,expected', (
    (lead_generation.FOOD_IS_GREAT,  lead_generation.SINGAPORE, 200),
    (lead_generation.FOOD_IS_GREAT,  lead_generation.FRANCE,    200),
    (lead_generation.LEGAL_IS_GREAT, lead_generation.SINGAPORE, 200),
    (lead_generation.LEGAL_IS_GREAT, lead_generation.FRANCE,    200),
    ('food-is-ungreat',      lead_generation.SINGAPORE, 404),
    (lead_generation.FOOD_IS_GREAT,  'themoon',         404),

))
def test_lead_generation_submit_campaign_country(
    showcase_objects, campaign, country, expected, client, settings
):
    settings.FEATURE_EXPORT_OPPORTUNITY_LEAD_GENERATION_ENABLED = True

    url = reverse(
        'lead-generation-submit',
        kwargs={'campaign': campaign, 'country': country}
    )
    response = client.get(url)

    assert response.status_code == expected


@pytest.mark.parametrize('url,languages', (
    (
        reverse('food-is-great-campaign-france'),
        [('en-gb', 'English'), ('fr', 'Français')]
    ),
    (
        reverse('food-is-great-campaign-singapore'),
        [('en-gb', 'English'), ('fr', 'Français')]
    ),
    (
        reverse('legal-is-great-campaign-singapore'),
        [('en-gb', 'English'), ('fr', 'Français')]
    ),
    (
        reverse('legal-is-great-campaign-singapore'),
        [('en-gb', 'English'), ('fr', 'Français')]
    ),
))
def test_campaign_language_switcher(
    showcase_objects, client, url, languages, settings
):
    settings.FEATURE_EXPORT_OPPORTUNITY_LEAD_GENERATION_ENABLED = True
    settings.FOOD_IS_GREAT_ENABLED_LANGUAGES = ['en-gb', 'fr']

    response = client.get(url)
    form = response.context['language_switcher']['form']

    assert response.context['language_switcher']['show'] is True
    assert form.fields['lang'].choices == languages


@patch.object(views.helpers, 'get_showcase_companies',
              return_value=showcase_companies)
@patch.object(views.api_client.exportopportunity, 'create_opportunity')
def test_submit_export_opportunity_food(
    mock_create_opportunity, mock_get_showcase_companies, client,
    api_response_200, settings, captcha_stub
):
    settings.FEATURE_EXPORT_OPPORTUNITY_LEAD_GENERATION_ENABLED = True
    mock_create_opportunity.return_value = api_response_200
    view = views.SubmitExportOpportunityWizardView
    url = reverse(
        'lead-generation-submit',
        kwargs={
            'campaign': lead_generation.FOOD_IS_GREAT,
            'country': lead_generation.FRANCE
        }
    )
    view_name = 'submit_export_opportunity_wizard_view'

    client.post(
        url,
        {
            view_name + '-current_step': view.SECTOR,
            view.SECTOR + '-business_model': 'distribution',
            view.SECTOR + '-business_model_other': 'things',
            view.SECTOR + '-target_sectors': 'retail',
            view.SECTOR + '-target_sectors_other': 'things',
            view.SECTOR + '-locality': lead_generation.FRANCE,
        }
    )
    client.post(
        url,
        {
            view_name + '-current_step': view.NEEDS,
            view.NEEDS + '-products': ['DISCOUNT'],
            view.NEEDS + '-products_other': 'things',
            view.NEEDS + '-order_size': '1-1000',
            view.NEEDS + '-order_deadline': '1-3 MONTHS',
            view.NEEDS + '-additional_requirements': 'give me things',
        }
    )
    response = client.post(
        url,
        {
            view_name + '-current_step': view.CONTACT,
            view.CONTACT + '-full_name': 'jim example',
            view.CONTACT + '-job_title': 'Exampler',
            view.CONTACT + '-email_address': 'jim@exmaple.com',
            view.CONTACT + '-email_address_confirm': 'jim@exmaple.com',
            view.CONTACT + '-company_name': 'Jim corp',
            view.CONTACT + '-company_website': 'http://www.example.com',
            view.CONTACT + '-phone_number': '07507605844',
            view.CONTACT + '-contact_preference': ['EMAIL', 'PHONE'],
            view.CONTACT + '-terms_agreed': True,
            'recaptcha_response_field': captcha_stub,
        }
    )

    assert response.status_code == 200
    assert response.template_name == (
        'exportopportunity/lead-generation-success-food.html'
    )
    assert response.context['industry'] == 'FOOD_AND_DRINK'
    assert response.context['companies'] == showcase_companies
    assert mock_create_opportunity.call_count == 1
    assert mock_create_opportunity.call_args == call(
        form_data={
            'additional_requirements': 'give me things',
            'business_model': ['distribution'],
            'business_model_other': 'things',
            'captcha': None,
            'company_name': 'Jim corp',
            'company_website': 'http://www.example.com',
            'contact_preference': ['EMAIL', 'PHONE'],
            'email_address': 'jim@exmaple.com',
            'email_address_confirm': 'jim@exmaple.com',
            'full_name': 'jim example',
            'job_title': 'Exampler',
            'locality': lead_generation.FRANCE,
            'order_deadline': '1-3 MONTHS',
            'order_size': '1-1000',
            'phone_number': '07507605844',
            'products': ['DISCOUNT'],
            'products_other': 'things',
            'target_sectors': ['retail'],
            'target_sectors_other': 'things',
            'terms_agreed': True,
            'campaign': lead_generation.FOOD_IS_GREAT,
            'country': lead_generation.FRANCE,
        }
    )
    assert mock_get_showcase_companies.call_count == 1
    assert mock_get_showcase_companies.call_args == call(
        sector='FOOD_AND_DRINK'
    )
