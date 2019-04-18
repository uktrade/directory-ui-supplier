from directory_api_client.client import api_client
import directory_components.helpers

from django.shortcuts import Http404


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
        }
