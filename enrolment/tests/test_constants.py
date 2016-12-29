from enrolment import constants

from directory_validators.constants.choices import COMPANY_CLASSIFICATIONS

valid_sectors = dict(COMPANY_CLASSIFICATIONS)


def test_sector_values_exist():
    assert constants.HEALTH_SECTOR_CONTEXT['sector_value'] in valid_sectors
    assert constants.TECH_SECTOR_CONTEXT['sector_value'] in valid_sectors
    assert constants.CREATIVE_SECTOR_CONTEXT['sector_value'] in valid_sectors
    assert constants.FOOD_SECTOR_CONTEXT['sector_value'] in valid_sectors


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
