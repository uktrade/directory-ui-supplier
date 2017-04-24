import json

import jsonschema
import pytest

from ui import helpers


def test_parse_sector_links_valid():
    valid = {
        'CREATIVE_AND_MEDIA': {
            'company_one': 'https://www.example.com',
            'company_two': 'http://www.example.com',
            'case_study': 'http://www.example.com'
        },
        'HEALTHCARE_AND_MEDICAL': {
            'company_one': 'http://www.example.com',
            'company_two': 'http://www.example.com',
            'case_study': 'http://www.example.com'
        },
        'FOOD_AND_DRINK': {
            'company_one': 'http://www.example.com',
            'company_two': 'http://www.example.com',
            'case_study': 'http://www.example.com'
        },
        'SOFTWARE_AND_COMPUTER_SERVICES': {
            'company_one': 'http://www.example.com',
            'company_two': 'http://www.example.com',
            'case_study': 'http://www.example.com'
        },
        'GLOBAL_SPORTS_INFRASTRUCTURE': {
            'company_one': 'http://www.example.com',
            'company_two': 'http://www.example.com',
            'case_study': 'http://www.example.com'
        }
    }

    actual = helpers.parse_sector_links(json.dumps(valid))
    assert actual == valid


def test_parse_sector_links_missing_sector():
    invalid = {
        'CREATIVE_AND_MEDIA': {
            'company_one': 'https://www.example.com',
            'company_two': 'http://www.example.com',
            'case_study': 'http://www.example.com'
        },
        'HEALTHCARE_AND_MEDICAL': {
            'company_one': 'http://www.example.com',
            'company_two': 'http://www.example.com',
            'case_study': 'http://www.example.com'
        },
        'FOOD_AND_DRINK': {
            'company_one': 'http://www.example.com',
            'company_two': 'http://www.example.com',
            'case_study': 'http://www.example.com'
        },
        # note the absence of SOFTWARE_AND_COMPUTER_SERVICES
    }

    with pytest.raises(jsonschema.exceptions.ValidationError):
        helpers.parse_sector_links(json.dumps(invalid))


def test_parse_sector_links_missing_key():
    invalid = {
        'CREATIVE_AND_MEDIA': {
            'company_one': 'https://www.example.com',
            'company_two': 'http://www.example.com',
            # note the absence case_study
        },
        'HEALTHCARE_AND_MEDICAL': {
            'company_one': 'http://www.example.com',
            'company_two': 'http://www.example.com',
            'case_study': 'http://www.example.com'
        },
        'FOOD_AND_DRINK': {
            'company_one': 'http://www.example.com',
            'company_two': 'http://www.example.com',
            'case_study': 'http://www.example.com'
        },
        'SOFTWARE_AND_COMPUTER_SERVICES': {
            'company_one': 'http://www.example.com',
            'company_two': 'http://www.example.com',
            'case_study': 'http://www.example.com'
        }
    }

    with pytest.raises(jsonschema.exceptions.ValidationError):
        helpers.parse_sector_links(json.dumps(invalid))


def test_parse_sector_links_missing():
    invalid = {}

    with pytest.raises(jsonschema.exceptions.ValidationError):
        helpers.parse_sector_links(json.dumps(invalid))
