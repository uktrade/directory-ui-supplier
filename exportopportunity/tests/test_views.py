from unittest.mock import call, patch, Mock

from directory_constants.constants import lead_generation, sectors
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
    url = reverse('food-is-great-lead-generation-submit-france')
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


@pytest.mark.parametrize('url,sector,query,template_name,search_keyword', (
    (
        reverse('food-is-great-campaign-france'),
        sectors.FOOD_AND_DRINK,
        {'sector': sectors.FOOD_AND_DRINK},
        'exportopportunity/campaign-food.html',
        '',
    ),
    (
        reverse('food-is-great-campaign-singapore'),
        sectors.FOOD_AND_DRINK,
        {'sector': sectors.FOOD_AND_DRINK},
        'exportopportunity/campaign-food.html',
        '',
    ),
    (
        reverse('legal-is-great-campaign-france'),
        'LEGAL',
        {'campaign_tag': lead_generation.LEGAL_IS_GREAT},
        'exportopportunity/campaign-legal.html',
        'legal',
    ),
    (
        reverse('legal-is-great-campaign-singapore'),
        'LEGAL',
        {'campaign_tag': lead_generation.LEGAL_IS_GREAT},
        'exportopportunity/campaign-legal.html',
        'legal',
    ),
))
@patch.object(views.helpers, 'get_showcase_companies',
              return_value=showcase_companies)
@patch.object(views.helpers, 'get_showcase_case_studies',
              return_value=showcase_case_studies)
def test_exportopportunity_view_context(
    mock_get_showcase_case_studies, mock_get_showcase_companies, url, sector,
    query, template_name, client, settings, search_keyword
):
    settings.FEATURE_EXPORT_OPPORTUNITY_LEAD_GENERATION_ENABLED = True

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [template_name]
    assert response.context['industry'] == sector
    assert response.context['companies'] == showcase_companies
    assert response.context['case_studies'] == showcase_case_studies
    assert response.context['search_keyword'] == search_keyword
    assert mock_get_showcase_companies.call_count == 1
    assert mock_get_showcase_companies.call_args == call(**query)
    assert mock_get_showcase_case_studies.call_count == 1
    assert mock_get_showcase_case_studies.call_args == call(**query)


@pytest.mark.parametrize('url,disabled_countries,expected', (
    (
        reverse('legal-is-great-campaign-singapore'),
        ['france', 'singapore'],
        False
    ),
    (
        reverse('legal-is-great-campaign-france'),
        ['france', 'singapore'],
        False
    ),
    (reverse('legal-is-great-campaign-singapore'), ['france'], True),
    (reverse('legal-is-great-campaign-france'),    ['france'], False),
    (reverse('legal-is-great-campaign-singapore'), ['singapore'], False),
    (reverse('legal-is-great-campaign-france'),    ['singapore'], True),
))
@patch.object(views.helpers, 'get_showcase_companies',
              return_value=showcase_companies)
@patch.object(views.helpers, 'get_showcase_case_studies',
              return_value=showcase_case_studies)
def test_exportopportunity_disabled_countries_lead_generation_legal(
    mock_get_showcase_case_studies, mock_get_showcase_companies,
    disabled_countries, expected, url, client, settings
):
    settings.FEATURE_EXPORT_OPPORTUNITY_LEAD_GENERATION_ENABLED = True
    settings.LEGAL_CAMPAIGN_DISABLED_COUNTRIES = disabled_countries
    response = client.get(url)

    assert response.status_code == 200
    assert response.context['is_lead_generation_enabled'] == expected


@pytest.mark.parametrize('url,disabled_countries,expected', (
    (
        reverse('food-is-great-campaign-singapore'),
        ['france', 'singapore'],
        False
    ),
    (
        reverse('food-is-great-campaign-france'),
        ['france', 'singapore'],
        False
    ),
    (reverse('food-is-great-campaign-singapore'), ['france'], True),
    (reverse('food-is-great-campaign-france'),    ['france'], False),
    (reverse('food-is-great-campaign-singapore'), ['singapore'], False),
    (reverse('food-is-great-campaign-france'),    ['singapore'], True),
))
@patch.object(views.helpers, 'get_showcase_companies',
              return_value=showcase_companies)
@patch.object(views.helpers, 'get_showcase_case_studies',
              return_value=showcase_case_studies)
def test_exportopportunity_disabled_countries_lead_generation_food(
    mock_get_showcase_case_studies, mock_get_showcase_companies,
    disabled_countries, expected, url, client, settings
):
    settings.FEATURE_EXPORT_OPPORTUNITY_LEAD_GENERATION_ENABLED = True
    settings.FOOD_CAMPAIGN_DISABLED_COUNTRIES = disabled_countries

    response = client.get(url)

    assert response.status_code == 200
    assert response.context['is_lead_generation_enabled'] == expected


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


@pytest.mark.parametrize('url,country', (
    (
        reverse('food-is-great-lead-generation-submit-france'),
        lead_generation.FRANCE,
    ),
    (
        reverse('food-is-great-lead-generation-submit-singapore'),
        lead_generation.SINGAPORE,
    ),
))
@patch.object(views.helpers, 'get_showcase_companies',
              return_value=showcase_companies)
@patch.object(views.api_client.exportopportunity, 'create_opportunity_food')
@patch('captcha.fields.ReCaptchaField.clean')
def test_submit_export_opportunity_food(
    mock_clean_captcha, mock_create_opportunity, mock_get_showcase_companies,
    client, api_response_200, settings, captcha_stub, url, country
):
    settings.FEATURE_EXPORT_OPPORTUNITY_LEAD_GENERATION_ENABLED = True
    mock_create_opportunity.return_value = api_response_200
    view_class = views.FoodIsGreatOpportunityWizardView
    view_name = 'food_is_great_opportunity_wizard_view'
    client.post(
        url,
        {
            view_name + '-current_step': view_class.SECTOR,
            view_class.SECTOR + '-business_model': 'distribution',
            view_class.SECTOR + '-business_model_other': 'things',
            view_class.SECTOR + '-target_sectors': 'retail',
            view_class.SECTOR + '-target_sectors_other': 'things',
            view_class.SECTOR + '-locality': country,
        }
    )
    client.post(
        url,
        {
            view_name + '-current_step': view_class.NEEDS,
            view_class.NEEDS + '-products': ['DISCOUNT'],
            view_class.NEEDS + '-products_other': 'things',
            view_class.NEEDS + '-order_size': '1-1000',
            view_class.NEEDS + '-order_deadline': '1-3 MONTHS',
            view_class.NEEDS + '-additional_requirements': 'give me things',
        }
    )
    response = client.post(
        url,
        {
            view_name + '-current_step': view_class.CONTACT,
            view_class.CONTACT + '-full_name': 'jim example',
            view_class.CONTACT + '-job_title': 'Exampler',
            view_class.CONTACT + '-email_address': 'jim@exmaple.com',
            view_class.CONTACT + '-email_address_confirm': 'jim@exmaple.com',
            view_class.CONTACT + '-company_name': 'Jim corp',
            view_class.CONTACT + '-company_website': 'http://www.example.com',
            view_class.CONTACT + '-phone_number': '07507605844',
            view_class.CONTACT + '-contact_preference': ['EMAIL', 'PHONE'],
            view_class.CONTACT + '-terms_agreed': True,
            'recaptcha_response_field': captcha_stub,
        }
    )

    assert response.status_code == 200
    assert response.template_name == (
        'exportopportunity/lead-generation-success-food.html'
    )
    assert response.context['industry'] == sectors.FOOD_AND_DRINK
    assert response.context['companies'] == showcase_companies
    assert mock_create_opportunity.call_count == 1
    assert mock_create_opportunity.call_args == call(
        form_data={
            'additional_requirements': 'give me things',
            'business_model': ['distribution'],
            'business_model_other': 'things',
            'company_name': 'Jim corp',
            'company_website': 'http://www.example.com',
            'contact_preference': ['EMAIL', 'PHONE'],
            'email_address': 'jim@exmaple.com',
            'email_address_confirm': 'jim@exmaple.com',
            'full_name': 'jim example',
            'job_title': 'Exampler',
            'locality': country,
            'order_deadline': '1-3 MONTHS',
            'order_size': '1-1000',
            'phone_number': '07507605844',
            'products': ['DISCOUNT'],
            'products_other': 'things',
            'target_sectors': ['retail'],
            'target_sectors_other': 'things',
            'terms_agreed': True,
            'campaign': lead_generation.FOOD_IS_GREAT,
            'country': country,
        }
    )
    assert mock_get_showcase_companies.call_count == 1
    assert mock_get_showcase_companies.call_args == call(
        sector=sectors.FOOD_AND_DRINK
    )
    assert mock_clean_captcha.call_count == 1


@pytest.mark.parametrize('url,country', (
    (
        reverse('legal-is-great-lead-generation-submit-france'),
        lead_generation.FRANCE,
    ),
    (
        reverse('legal-is-great-lead-generation-submit-singapore'),
        lead_generation.SINGAPORE,
    ),
))
@patch.object(views.helpers, 'get_showcase_companies',
              return_value=showcase_companies)
@patch.object(views.api_client.exportopportunity, 'create_opportunity_legal')
@patch('captcha.fields.ReCaptchaField.clean')
def test_submit_export_opportunity_legal(
    mock_clean_captcha, mock_create_opportunity, mock_get_showcase_companies,
    client, api_response_200, settings, captcha_stub, url, country
):
    settings.FEATURE_EXPORT_OPPORTUNITY_LEAD_GENERATION_ENABLED = True
    mock_create_opportunity.return_value = api_response_200
    view_class = views.LegalIsGreatOpportunityWizardView
    view_name = 'legal_is_great_opportunity_wizard_view'
    client.post(
        url,
        {
            view_name + '-current_step': view_class.SECTOR,
            view_class.SECTOR + '-advice_type': ['Business-start-up-advice'],
            view_class.SECTOR + '-advice_type_other': 'things',
            view_class.SECTOR + '-target_sectors': sectors.TECHNOLOGY,
            view_class.SECTOR + '-target_sectors_other': 'things',
            view_class.SECTOR + '-locality': country,
        }
    )
    client.post(
        url,
        {
            view_name + '-current_step': view_class.NEEDS,
            view_class.NEEDS + '-order_deadline': '1-3 MONTHS',
            view_class.NEEDS + '-additional_requirements': 'give me things',
        }
    )
    response = client.post(
        url,
        {
            view_name + '-current_step': view_class.CONTACT,
            view_class.CONTACT + '-full_name': 'jim example',
            view_class.CONTACT + '-job_title': 'Exampler',
            view_class.CONTACT + '-email_address': 'jim@exmaple.com',
            view_class.CONTACT + '-email_address_confirm': 'jim@exmaple.com',
            view_class.CONTACT + '-company_name': 'Jim corp',
            view_class.CONTACT + '-company_website': 'http://www.example.com',
            view_class.CONTACT + '-phone_number': '07507605844',
            view_class.CONTACT + '-contact_preference': ['EMAIL', 'PHONE'],
            view_class.CONTACT + '-terms_agreed': True,
            'recaptcha_response_field': captcha_stub,
        }
    )

    assert response.status_code == 200
    assert response.template_name == (
        'exportopportunity/lead-generation-success-legal.html'
    )
    assert response.context['industry'] == sectors.LEGAL
    assert response.context['companies'] == showcase_companies
    assert mock_create_opportunity.call_count == 1
    assert mock_create_opportunity.call_args == call(
        form_data={
           'company_name': 'Jim corp',
           'full_name': 'jim example',
           'phone_number': '07507605844',
           'advice_type_other': 'things',
           'campaign': 'legal-is-great',
           'job_title': 'Exampler',
           'contact_preference': ['EMAIL', 'PHONE'],
           'target_sectors_other': 'things',
           'order_deadline': '1-3 MONTHS',
           'country': country,
           'email_address': 'jim@exmaple.com',
           'email_address_confirm': 'jim@exmaple.com',
           'target_sectors': ['TECHNOLOGY'],
           'advice_type': ['Business-start-up-advice'],
           'locality': country,
           'terms_agreed': True,
           'company_website': 'http://www.example.com',
           'additional_requirements': 'give me things'
        }
    )
    assert mock_get_showcase_companies.call_count == 1
    assert mock_get_showcase_companies.call_args == call(
        campaign_tag=lead_generation.LEGAL_IS_GREAT,
    )

    assert mock_clean_captcha.call_count == 1
