import json

import jsonschema

from django.utils import translation


def parse_sector_links(raw):
    # http://jsonschema.net/
    sectors = [
        'CREATIVE_AND_MEDIA',
        'HEALTHCARE_AND_MEDICAL',
        'FOOD_AND_DRINK',
        'SOFTWARE_AND_COMPUTER_SERVICES',
        'GLOBAL_SPORTS_INFRASTRUCTURE',
    ]
    sector_schema = {
        'type': 'object',
        'properties': {
            'company_one': {'type': 'string'},
            'company_two': {'type': 'string'},
            'case_study': {'type': 'string'}
        },
        'required': ['company_one', 'company_two', 'case_study'],
    }
    parsed = json.loads(raw)
    # side effect: raises ValidationError if `raw` was not expected schema
    jsonschema.validate(parsed, {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'type': 'object',
        'properties': {sector: sector_schema for sector in sectors},
        'required': sectors,
    })
    return parsed


def get_language_from_querystring(request):
    language_code = request.GET.get('lang')
    language_codes = translation.trans_real.get_languages()
    if language_code and language_code in language_codes:
        return language_code


def remove_disabled_languages(disabled_languages, languages):
    return [
        (key, name) for key, name in languages if key not in disabled_languages
    ]
