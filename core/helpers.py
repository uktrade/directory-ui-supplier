import collections

from directory_api_client.client import api_client
from directory_constants import choices
import directory_components
import directory_components.helpers

from django.shortcuts import Http404
from django.utils import translation
from django.utils.html import escape, mark_safe


NotifySettings = collections.namedtuple(
    'NotifySettings',
    [
        'company_template',
        'support_template',
        'investor_template',
        'support_email_address',
    ]
)


def handle_cms_response(response):
    if response.status_code == 404:
        raise Http404()
    response.raise_for_status()
    return response.json()


def get_language_from_querystring(request):
    language_code = request.GET.get('language') or request.GET.get('lang')
    language_codes = translation.trans_real.get_languages()
    if language_code and language_code in language_codes:
        return language_code


def get_company_profile(number):
    response = api_client.company.retrieve_public_profile(number=number)
    if response.status_code == 404:
        raise Http404(f'API returned 404 for company number {number}')
    response.raise_for_status()
    return response.json()


class CompanyParser(directory_components.helpers.CompanyParser):

    def serialize_for_template(self):
        if not self.data:
            return {}
        return {
            **self.data,
            'date_of_creation': self.date_of_creation,
            'address': self.address,
            'sectors': self.sectors_label,
            'keywords': self.keywords,
            'employees': self.employees_label,
            'expertise_industries': self.expertise_industries_label,
            'expertise_regions': self.expertise_regions_label,
            'expertise_countries': self.expertise_countries_label,
            'expertise_languages': self.expertise_languages_label,
            'has_expertise': self.has_expertise,
            'expertise_products_services': (
                self.expertise_products_services_label
            ),
            'is_in_companies_house': self.is_in_companies_house,
        }


def get_results_from_search_response(response):
    parsed = response.json()
    formatted_results = []

    for result in parsed['hits']['hits']:
        parser = CompanyParser(result['_source'])
        formatted = parser.serialize_for_template()
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


def get_filters_labels(filters):
    sectors = dict(choices.INDUSTRIES)
    languages = dict(choices.EXPERTISE_LANGUAGES)
    labels = []
    skip_fields = [
        'q',
        'page',
        # Prevents duplicates labels not to be displayed in filter list
        'expertise_products_services_label'
    ]
    for name, values in filters.items():
        if name in skip_fields:
            pass
        elif name == 'industries':
            labels += [sectors[item] for item in values if item in sectors]
        elif name == 'expertise_languages':
            labels += [languages[item] for item in values if item in languages]
        elif name.startswith('expertise_products_services_'):
            labels += values
        else:
            for value in values:
                labels.append(value.replace('_', ' ').title())
    return labels
