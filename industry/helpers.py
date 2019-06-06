from directory_api_client.client import api_client

from core.helpers import CompanyParser


def get_showcase_companies(**kwargs):
    response = api_client.company.search_company(page=1, **kwargs)
    response.raise_for_status()
    formatted = []
    for result in response.json()['hits']['hits']:
        parser = CompanyParser(result['_source'])
        formatted.append(parser.serialize_for_template())
    return formatted
