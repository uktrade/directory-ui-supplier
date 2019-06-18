import requests
import pytest

from django.urls import reverse

from find_a_supplier import helpers
from core.helpers import CompanyParser


@pytest.fixture
def public_companies(retrieve_profile_data):
    return {
        'count': 100,
        'results': [retrieve_profile_data]
    }


@pytest.fixture
def public_companies_empty():
    return {
        'count': 0,
        'results': []
    }


def test_pair_sector_values_with_label():
    values = ['AGRICULTURE_HORTICULTURE_AND_FISHERIES', 'AEROSPACE']
    expected = [
        {
            'label': 'Agriculture, horticulture and fisheries',
            'value': 'AGRICULTURE_HORTICULTURE_AND_FISHERIES',
        },
        {
            'label': 'Aerospace',
            'value': 'AEROSPACE',
        }
    ]
    assert helpers.pair_sector_values_with_label(values) == expected


def test_pair_sector_values_with_label_contains_invalid():
    values = ['AGRICULTURE_HORTICULTURE_AND_FISHERIES', 'AEROSPACE', 'DEFENCE']
    expected = [
        {
            'label': 'Agriculture, horticulture and fisheries',
            'value': 'AGRICULTURE_HORTICULTURE_AND_FISHERIES',
        },
        {
            'label': 'Aerospace',
            'value': 'AEROSPACE',
        },
    ]

    assert helpers.pair_sector_values_with_label(values) == expected


def test_pair_sector_values_with_label_empty():
    for value in [None, []]:
        assert helpers.pair_sector_values_with_label(value) == []


def test_format_case_study():
    case_study = {
        'sector': 'AEROSPACE',
        'pk': '1',
        'slug': 'good-stuff',
    }
    expected = {
        'sector': {
            'label': 'Aerospace',
            'value': 'AEROSPACE',
        },
        'pk': '1',
        'slug': 'good-stuff',
        'case_study_url': '/trade/case-study/1/good-stuff/'
    }
    actual = helpers.format_case_study(case_study)
    assert actual == expected


def test_get_case_study_details_from_response(supplier_case_study_data):
    response = requests.Response()
    response.json = lambda: supplier_case_study_data

    company = CompanyParser(supplier_case_study_data['company'])
    expected = {
        'description': 'Damn great',
        'year': '2000',
        'title': 'Two',
        'sector': {
            'value': 'SOFTWARE_AND_COMPUTER_SERVICES',
            'label': 'Software and computer services',
        },
        'testimonial': 'I found it most pleasing.',
        'keywords': 'great',
        'image_three': 'https://image_three.jpg',
        'pk': 2,
        'website': 'http://www.google.com',
        'image_two': 'https://image_two.jpg',
        'company': company.serialize_for_template(),
        'slug': 'two',
        'image_one': 'https://image_one.jpg',
        'video_one': 'https://video_one.wav',
    }
    assert helpers.get_case_study_details_from_response(response) == expected


def test_get_paginator_url():
    filters = {'page': 2, 'term': 'foo', 'industries': None}

    assert helpers.get_paginator_url(filters) == (
        reverse('find-a-supplier:search') + '?term=foo'
    )


def test_get_paginator_url_multiple_filters():
    filters = {
        'industries': ['AEROSPACE', 'AGRICULTURE_HORTICULTURE_AND_FISHERIES'],
    }

    encoded_url = (
        '?industries=AEROSPACE'
        '&industries=AGRICULTURE_HORTICULTURE_AND_FISHERIES'
    )

    assert helpers.get_paginator_url(filters) == (
            reverse('find-a-supplier:search') + encoded_url
    )
