from directory_api_client.client import api_client
from directory_constants import choices

from django.http import Http404
from django.core.urlresolvers import reverse

from core.helpers import CompanyParser


INDUSTRY_CHOICES = dict(choices.INDUSTRIES)


def pair_sector_values_with_label(sectors_values):
    if not sectors_values:
        return []
    return [
        pair_sector_value_with_label(value) for value in sectors_values
        if value in INDUSTRY_CHOICES
    ]


def pair_sector_value_with_label(sectors_value):
    return {'value': sectors_value, 'label': get_sectors_label(sectors_value)}


def get_sectors_label(sectors_value):
    if not sectors_value:
        return sectors_value
    return INDUSTRY_CHOICES.get(sectors_value)


def get_case_study_details_from_response(response):
    parsed = response.json()
    # `format_company_details` expects `supplier_case_studies` key.
    parsed['company']['supplier_case_studies'] = []
    parsed['sector'] = pair_sector_value_with_label(parsed['sector'])
    parsed['company'] = CompanyParser(
        parsed['company']
    ).serialize_for_template()
    return parsed


def format_case_study(case_study):
    case_study_url = reverse(
        'case-study-details',
        kwargs={'id': case_study['pk'], 'slug': case_study['slug']},
    )
    return {
        **case_study,
        'sector': pair_sector_value_with_label(case_study['sector']),
        'case_study_url': case_study_url,
    }


def get_case_study(case_study_id):
    response = api_client.company.retrieve_public_case_study(case_study_id)
    if response.status_code == 404:
        raise Http404(
            "API returned 404 for case study with id %s", case_study_id,
        )
    response.raise_for_status()
    return get_case_study_details_from_response(response)
