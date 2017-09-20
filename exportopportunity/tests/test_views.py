import pytest
from unittest.mock import call, patch

from django.core.urlresolvers import reverse

from exportopportunity import views


exportopportunity_urls = (
    reverse(
        'lead-generation-submit',
        kwargs={'campaign': 'food-is-great', 'country': 'france'}
    ),
    reverse(
        'campaign', kwargs={'campaign': 'food-is-great', 'country': 'france'}
    ),
)


@pytest.mark.parametrize('url', exportopportunity_urls)
def test_exportopportunity_view_feature_flag_off(url, client, settings):
    settings.FEATURE_EXPORT_OPPORTUNITY_LEAD_GENERATION_ENABLED = False

    response = client.get(url)

    assert response.status_code == 404


@patch.object(views.helpers, 'get_showcase_companies',
              return_value=[{'name': 'Showcase company 1'}])
def test_exportopportunity_view_context(
    mock_get_showcase_companies, client, settings
):
    settings.FEATURE_EXPORT_OPPORTUNITY_LEAD_GENERATION_ENABLED = True
    url = reverse(
        'campaign', kwargs={'campaign': 'food-is-great', 'country': 'france'}
    )

    response = client.get(url)

    assert response.status_code == 200

    assert response.context['industry'] == 'FOOD_AND_DRINK'
    assert response.context['companies'] == [{'name': 'Showcase company 1'}]
    assert mock_get_showcase_companies.call_count == 1
    assert mock_get_showcase_companies.call_args == call(
        sector='FOOD_AND_DRINK'
    )


def test_campaign_invalid_campaign(client, settings):
    settings.FEATURE_EXPORT_OPPORTUNITY_LEAD_GENERATION_ENABLED = True

    url = reverse(
        'campaign',
        kwargs={'campaign': 'food-is-not-great', 'country': 'france'}
    )
    response = client.get(url)

    assert response.status_code == 404


def test_lead_generation_submit_invalid_campaign(client, settings):
    settings.FEATURE_EXPORT_OPPORTUNITY_LEAD_GENERATION_ENABLED = True

    url = reverse(
        'lead-generation-submit',
        kwargs={'campaign': 'food-is-not-great', 'country': 'france'}
    )
    response = client.get(url)

    assert response.status_code == 404


@patch.object(views.helpers, 'get_showcase_companies',
              return_value=[{'name': 'Showcase company 1'}])
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
        kwargs={'campaign': 'food-is-great', 'country': 'france'}
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
            view.SECTOR + '-locality': 'France',
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
    assert response.context['companies'] == [{'name': 'Showcase company 1'}]
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
            'locality': 'France',
            'order_deadline': '1-3 MONTHS',
            'order_size': '1-1000',
            'phone_number': '07507605844',
            'products': ['DISCOUNT'],
            'products_other': 'things',
            'target_sectors': ['retail'],
            'target_sectors_other': 'things',
            'terms_agreed': True,
            'campaign': 'food-is-great',
            'country': 'france',
        }
    )
    assert mock_get_showcase_companies.call_count == 1
    assert mock_get_showcase_companies.call_args == call(
        sector='FOOD_AND_DRINK'
    )
