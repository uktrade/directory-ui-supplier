from api_client import api_client

from company.helpers import format_company_details


def get_showcase_companies(sector):
    response = api_client.company.search(
        term="", page=1, sectors=sector, size=3,
    )
    response.raise_for_status()
    parsed = response.json()
    formatted = []
    for result in parsed['hits']['hits']:
        formatted.append(format_company_details(result['_source']))
    return formatted
