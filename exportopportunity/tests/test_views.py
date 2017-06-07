from django.core.urlresolvers import reverse

from exportopportunity import views


def test_exportopportunity_view_feature_flag_on(client, settings):
    settings.FEATURE_EXPORT_OPPORTUNITY_LEAD_GENERATION_ENABLED = False

    response = client.get(reverse('export-opportunity'))

    assert response.status_code == 404


def test_exportopportunity_view_feature_flag_off(client, settings):
    settings.FEATURE_EXPORT_OPPORTUNITY_LEAD_GENERATION_ENABLED = True
    expected_template_name = views.SubmitExportOpportunityView.template_name

    response = client.get(reverse('export-opportunity'))

    assert response.status_code == 200
    assert response.template_name == [expected_template_name]
