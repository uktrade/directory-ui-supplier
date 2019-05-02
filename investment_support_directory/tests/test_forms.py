from directory_constants import choices
import pytest

from investment_support_directory import forms


prefix = 'expertise_products_services'


def test_company_search_form_expertise_products_services():
    form = forms.CompanySearchForm(data={
        'term': 'foo',
        f'{prefix}_management': [forms.CHOICES_MANAGEMENT_CONSULTING[0]],
        f'{prefix}_human_resources': [forms.CHOICES_HUMAN_RESOURCES[0]],
        f'{prefix}_legal': [forms.CHOICES_LEGAL[0]],
        f'{prefix}_publicity': [forms.CHOICES_PUBLICITY[0]],
        f'{prefix}_further_services': [forms.CHOICES_FURTHER_SERVICES[0]],
    })

    assert form.is_valid()
    assert form.cleaned_data['expertise_products_services_labels'] == [
        forms.CHOICES_MANAGEMENT_CONSULTING[0],
        forms.CHOICES_HUMAN_RESOURCES[0],
        forms.CHOICES_LEGAL[0],
        forms.CHOICES_PUBLICITY[0],
        forms.CHOICES_FURTHER_SERVICES[0],
    ]


def test_company_search_form_page_present():
    form = forms.CompanySearchForm(data={
        'q': 'foo',
        'page': 5,
    })
    assert form.is_valid()
    assert form.cleaned_data['page'] == 5


def test_company_search_form_page_missing():
    form = forms.CompanySearchForm(data={
        'q': 'foo',
    })
    assert form.is_valid()
    assert form.cleaned_data['page'] == 1


@pytest.mark.parametrize('data', (
    {'expertise_industries': [choices.INDUSTRIES[0][0]]},
    {'expertise_regions': [choices.EXPERTISE_REGION_CHOICES[0][0]]},
    {'expertise_countries': [choices.COUNTRY_CHOICES[0][0]]},
    {'expertise_languages': [choices.EXPERTISE_LANGUAGES[0][0]]},
    {'q': 'foo'},
    {f'{prefix}_management': [forms.CHOICES_MANAGEMENT_CONSULTING[0]]},
    {f'{prefix}_human_resources': [forms.CHOICES_HUMAN_RESOURCES[0]]},
    {f'{prefix}_legal': [forms.CHOICES_LEGAL[0]]},
    {f'{prefix}_publicity': [forms.CHOICES_PUBLICITY[0]]},
    {f'{prefix}_further_services': [forms.CHOICES_FURTHER_SERVICES[0]]},
))
def test_minimum_viable_search(data):
    form = forms.CompanySearchForm(data=data)

    assert form.is_valid()


def test_minimum_viable_search_failure():
    form = forms.CompanySearchForm(data={})

    assert form.is_valid() is False
    assert form.errors['q'] == [form.MESSAGE_MINIMUM_VIABLE_SEARCH]
