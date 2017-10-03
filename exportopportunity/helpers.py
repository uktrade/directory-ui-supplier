from api_client import api_client

from company.helpers import format_case_study, format_company_details


def get_showcase_resource(api_client_method, formatter, **kwargs):
    response = api_client_method(
        term="", page=1, size=3, **kwargs
    )
    response.raise_for_status()
    formatted = []
    for result in response.json()['hits']['hits']:
        formatted.append(formatter(result['_source']))
    return formatted


def get_showcase_companies(**kwargs):
    return get_showcase_resource(
        api_client_method=api_client.company.search_company,
        formatter=format_company_details,
        **kwargs,
    )


def get_showcase_case_studies(**kwargs):
    return get_showcase_resource(
        api_client_method=api_client.company.search_case_study,
        formatter=format_case_study,
        **kwargs,
    )
