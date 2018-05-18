from api_client import api_client

from company.helpers import format_company_details


def get_showcase_companies(**kwargs):
    response = api_client.company.search_company(page=1, **kwargs)
    response.raise_for_status()
    formatted = []
    for result in response.json()['hits']['hits']:
        formatted.append(format_company_details(result['_source']))
    return formatted
