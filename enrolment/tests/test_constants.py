from django.conf import settings

from enrolment import constants

from directory_constants.constants.choices import INDUSTRIES


valid_sectors = (
    [value for value, label in INDUSTRIES] +
    list(constants.SECTOR_FILTER_GROUPS.keys())
)


def test_sector_values_exist():
    assert constants.HEALTH_SECTOR_CONTEXT['sector_value'] in valid_sectors
    assert constants.TECH_SECTOR_CONTEXT['sector_value'] in valid_sectors
    assert constants.CREATIVE_SECTOR_CONTEXT['sector_value'] in valid_sectors
    assert constants.FOOD_SECTOR_CONTEXT['sector_value'] in valid_sectors


def test_sector_values_populates_correct_links():
    pairs = (
        ('HEALTHCARE_AND_MEDICAL', constants.HEALTH_SECTOR_CONTEXT),
        ('SOFTWARE_AND_COMPUTER_SERVICES', constants.TECH_SECTOR_CONTEXT),
        ('CREATIVE_AND_MEDIA', constants.CREATIVE_SECTOR_CONTEXT),
        ('FOOD_AND_DRINK', constants.FOOD_SECTOR_CONTEXT),
    )
    for sector_name, constant in pairs:
        links = settings.SECTOR_LINKS[sector_name]
        assert constant['case_study']['url'] == links['case_study']
        assert constant['companies'][0]['url'] == links['company_one']
        assert constant['companies'][1]['url'] == links['company_two']


def test_case_study_sectors_exist():
    contexts = [
        constants.HEALTH_SECTOR_CONTEXT,
        constants.TECH_SECTOR_CONTEXT,
        constants.CREATIVE_SECTOR_CONTEXT,
        constants.FOOD_SECTOR_CONTEXT,
    ]
    for context in contexts:
        for sector in context['case_study']['sectors']:
            assert sector['value'] in valid_sectors
