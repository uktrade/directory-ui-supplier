import pytest

from django.core.urlresolvers import reverse


exportopportunity_urls = (
    reverse('export-opportunity'),
    reverse('lead-generation-food'),
)


@pytest.mark.parametrize('url', exportopportunity_urls)
def test_exportopportunity_view_feature_flag_off(url, client, settings):
    settings.FEATURE_EXPORT_OPPORTUNITY_LEAD_GENERATION_ENABLED = False

    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.parametrize('url', exportopportunity_urls)
def test_exportopportunity_view_feature_flag_on(url, client, settings):
    settings.FEATURE_EXPORT_OPPORTUNITY_LEAD_GENERATION_ENABLED = True

    response = client.get(url)

    assert response.status_code == 200
