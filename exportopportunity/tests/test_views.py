from unittest import mock

from django.core.urlresolvers import reverse

from directory_constants.constants import choices

from exportopportunity import views


def test_exportopportunity_view_feature_flag_on(client, settings):
    settings.FEATURE_EXPORT_OPPORTUNITY_LEAD_GENERATION_ENABLED = False

    response = client.post(reverse('export-opportunity'))

    assert response.status_code == 404


@mock.patch('exportopportunity.views.api_client')
def test_exportopportunity_view_feature_flag_off(
        mock_api_client,
        client,
        settings,
        captcha_stub):
    settings.FEATURE_EXPORT_OPPORTUNITY_LEAD_GENERATION_ENABLED = True
    expected_template_name = views.SubmitExportOpportunityView.success_template

    data = {
        'recaptcha_response_field': captcha_stub,
        'type_of_enquiry': choices.OPEN_ENDED,
        'open_ended_description': 'foobar',
        'business_model': choices.DISTRIBUTION,
        'subsector': choices.CATERING,
        'bid_value': 'badzillions',
        'bid_timing': '2017-09-09',
        'full_name': 'Testo Useri',
        'email_address': 'test@foo.com',
        'company_name': 'Acme'
    }

    response = client.post(reverse('export-opportunity'), data=data)

    assert response.status_code == 200
    assert response.template_name == expected_template_name
    expected_data = {
        'captcha': None,
        'type_of_enquiry': choices.OPEN_ENDED,
        'open_ended_description': 'foobar',
        'business_model': choices.DISTRIBUTION,
        'subsector': choices.CATERING,
        'bid_value': 'badzillions',
        'bid_timing': '2017-09-09',
        'full_name': 'Testo Useri',
        'email_address': 'test@foo.com',
        'company_name': 'Acme'
    }
    mock_api_client.exportopportunity.create_opportunity.assert_called_with(
        form_data=expected_data
    )
