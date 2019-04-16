import datetime
import http

from directory_api_client.client import api_client
from directory_constants import choices
from directory_validators.helpers import tokenize_keywords

from django.http import Http404
from django.core.urlresolvers import reverse
from django.utils.html import escape, mark_safe


EMPLOYEE_CHOICES = dict(choices.EMPLOYEES)
INDUSTRY_CHOICES = dict(choices.INDUSTRIES)


def format_date_of_creation(raw_date_of_creation):
    if not raw_date_of_creation:
        return raw_date_of_creation
    return datetime.datetime.strptime(raw_date_of_creation, '%Y-%m-%d')


def format_date_modified(raw_date):
    if not raw_date:
        return raw_date
    return datetime.datetime.strptime(raw_date, '%Y-%m-%dT%H:%M:%S.%fZ')


def get_employees_label(employees_value):
    if not employees_value:
        return employees_value
    return EMPLOYEE_CHOICES.get(employees_value)


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
    parsed['company'] = format_company_details(parsed['company'])
    return parsed


def get_public_company_profile_from_response(response):
    return format_company_details(response.json())


def get_company_profile_from_response(response):
    return format_company_details(response.json())


def get_company_list_from_response(response):
    parsed = response.json()
    if parsed['results']:
        results = map(format_company_details, parsed['results'])
        parsed['results'] = list(results)
    return parsed


def get_results_from_search_response(response):
    parsed = response.json()
    formatted_results = []

    for result in parsed['hits']['hits']:
        formatted = format_company_details(result['_source'])
        if 'highlight' in result:
            highlighted = '...'.join(
                result['highlight'].get('description', '') or
                result['highlight'].get('summary', '')
            )
            # escape all html tags other than <em> and </em>
            highlighted_escaped = (
                escape(highlighted)
                .replace('&lt;em&gt;', '<em>')
                .replace('&lt;/em&gt;', '</em>')
            )
            formatted['highlight'] = mark_safe(highlighted_escaped)
        formatted_results.append(formatted)

    parsed['results'] = formatted_results
    return parsed


def format_company_details(details):
    date_of_creation = format_date_of_creation(details.get('date_of_creation'))
    case_studies = map(
        format_case_study, details.get('supplier_case_studies', [])
    )
    keywords = details['keywords']
    return {
        'website': details['website'],
        'description': details['description'],
        'summary': details['summary'],
        'number': details['number'],
        'date_of_creation': date_of_creation,
        'sectors': pair_sector_values_with_label(details.get('sectors', [])),
        'logo': details.get('logo'),
        'name': details['name'],
        'keywords': tokenize_keywords(keywords) if keywords else [],
        'employees': get_employees_label(details['employees']),
        'supplier_case_studies': list(case_studies),
        'modified': format_date_modified(details['modified']),
        'twitter_url': details['twitter_url'],
        'facebook_url': details['facebook_url'],
        'linkedin_url': details['linkedin_url'],
        'email_address': details.get('email_address'),
        'slug': details['slug'],
        'public_profile_url': reverse(
            'public-company-profiles-detail',
            kwargs={
                'company_number': details['number'],
                'slug': details['slug']
            }
        ),
        'has_social_links': bool(
            details['twitter_url'] or
            details['facebook_url'] or
            details['linkedin_url']
        ),
    }


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


def get_company_profile(number):
    response = api_client.company.retrieve_public_profile(number=number)
    if response.status_code == http.client.NOT_FOUND:
        raise Http404("API returned 404 for company number %s", number)
    response.raise_for_status()
    return get_public_company_profile_from_response(response)


def get_case_study(case_study_id):
    response = api_client.company.retrieve_public_case_study(
        case_study_id=case_study_id,
    )
    if response.status_code == http.client.NOT_FOUND:
        raise Http404(
            "API returned 404 for case study with id %s", case_study_id,
        )
    response.raise_for_status()
    return get_case_study_details_from_response(response)
