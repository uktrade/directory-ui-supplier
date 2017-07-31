from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import pytest

from django.core.urlresolvers import reverse

from company.templatetags import company_tags


def test_date_recency_empty_value():
    value = company_tags.date_recency('')

    assert value == ''


def test_date_recency_hours_plural():
    value = company_tags.date_recency(datetime.utcnow() - timedelta(hours=3))

    assert value == '3 hours ago'


def test_date_recency_days_plural():
    value = company_tags.date_recency(datetime.utcnow() - timedelta(days=5))

    assert value == '5 days ago'


def test_date_recency_months_plural():
    value = company_tags.date_recency(
        datetime.utcnow() - relativedelta(months=7)
    )

    assert value == '7 months ago'


def test_date_recency_years_plural_year():
    value = company_tags.date_recency(
        datetime.utcnow() - relativedelta(months=25)
    )

    assert value == '2 years and 1 month ago'


def test_date_recency_years_plural_month():
    value = company_tags.date_recency(
        datetime.utcnow() - relativedelta(months=14)
    )

    assert value == '1 year and 2 months ago'


def test_date_recency_hours_single():
    value = company_tags.date_recency(datetime.utcnow() - timedelta(hours=1))

    assert value == '1 hour ago'


def test_date_recency_days_single():
    value = company_tags.date_recency(datetime.utcnow() - timedelta(days=1))

    assert value == '1 day ago'


def test_date_recency_months_single():
    value = company_tags.date_recency(
        datetime.utcnow() - relativedelta(months=1)
    )

    assert value == '1 month ago'


@pytest.mark.parametrize('filter_value,expected', [
    ('AEROSPACE', '?sectors=AEROSPACE'),
    ('AGRICULTURE_HORTICULTURE_AND_FISHERIES',
        '?sectors=AGRICULTURE_HORTICULTURE_AND_FISHERIES'),
    ('AIRPORTS', '?sectors=AIRPORTS'),
    ('AUTOMOTIVE', '?sectors=AUTOMOTIVE'),
    ('BIOTECHNOLOGY_AND_PHARMACEUTICALS',
        '?sectors=BIOTECHNOLOGY_AND_PHARMACEUTICALS'),
    ('BUSINESS_AND_CONSUMER_SERVICES',
        '?sectors=BUSINESS_AND_CONSUMER_SERVICES'),
    ('CHEMICALS', '?sectors=CHEMICALS'),
    ('CLOTHING_FOOTWEAR_AND_FASHION',
        '?sectors=CLOTHING_FOOTWEAR_AND_FASHION'),
    ('COMMUNICATIONS', '?sectors=COMMUNICATIONS'),
    ('CONSTRUCTION', '?sectors=CONSTRUCTION'),
    ('CREATIVE_AND_MEDIA', '?sectors=CREATIVE_AND_MEDIA'),
    ('EDUCATION_AND_TRAINING', '?sectors=EDUCATION_AND_TRAINING'),
    ('ELECTRONICS_AND_IT_HARDWARE', '?sectors=ELECTRONICS_AND_IT_HARDWARE'),
    ('ENVIRONMENT', '?sectors=ENVIRONMENT'),
    ('FINANCIAL_AND_PROFESSIONAL_SERVICES',
        '?sectors=FINANCIAL_AND_PROFESSIONAL_SERVICES'),
    ('FOOD_AND_DRINK', '?sectors=FOOD_AND_DRINK'),
    ('GIFTWARE_JEWELLERY_AND_TABLEWARE',
        '?sectors=GIFTWARE_JEWELLERY_AND_TABLEWARE'),
    ('GLOBAL_SPORTS_INFRASTRUCTURE', '?sectors=GLOBAL_SPORTS_INFRASTRUCTURE'),
    ('HEALTHCARE_AND_MEDICAL', '?sectors=HEALTHCARE_AND_MEDICAL'),
    ('HOUSEHOLD_GOODS_FURNITURE_AND_FURNISHINGS',
        '?sectors=HOUSEHOLD_GOODS_FURNITURE_AND_FURNISHINGS'),
    ('LEISURE_AND_TOURISM', '?sectors=LEISURE_AND_TOURISM'),
    ('MARINE', '?sectors=MARINE'),
    ('MECHANICAL_ELECTRICAL_AND_PROCESS_ENGINEERING',
        '?sectors=MECHANICAL_ELECTRICAL_AND_PROCESS_ENGINEERING'),
    ('METALLURGICAL_PROCESS_PLANT', '?sectors=METALLURGICAL_PROCESS_PLANT'),
    ('METALS_MINERALS_AND_MATERIALS',
        '?sectors=METALS_MINERALS_AND_MATERIALS'),
    ('MINING', '?sectors=MINING'),
    ('OIL_AND_GAS', '?sectors=OIL_AND_GAS'),
    ('PORTS_AND_LOGISTICS', '?sectors=PORTS_AND_LOGISTICS'),
    ('POWER', '?sectors=POWER'),
    ('RAILWAYS', '?sectors=RAILWAYS'),
    ('RENEWABLE_ENERGY', '?sectors=RENEWABLE_ENERGY'),
    ('RETAIL_AND_LUXURY', '?sectors=RETAIL_AND_LUXURY'),
    ('SECURITY', '?sectors=SECURITY'),
    ('SOFTWARE_AND_COMPUTER_SERVICES',
        '?sectors=SOFTWARE_AND_COMPUTER_SERVICES'),
    ('TEXTILES_INTERIOR_TEXTILES_AND_CARPETS',
        '?sectors=TEXTILES_INTERIOR_TEXTILES_AND_CARPETS'),
    ('WATER', '?sectors=WATER'),
    (
        'ADVANCED_MANUFACTURING',
        (
            '?sectors=MECHANICAL_ELECTRICAL_AND_PROCESS_ENGINEERING'
            '&sectors=METALLURGICAL_PROCESS_PLANT'
            '&sectors=METALS_MINERALS_AND_MATERIALS'
            '&sectors=MINING'
        )
    ),
    (
        'CONSUMER_AND_RETAIL',
        (
            '?sectors=CLOTHING_FOOTWEAR_AND_FASHION'
            '&sectors=GIFTWARE_JEWELLERY_AND_TABLEWARE'
            '&sectors=HOUSEHOLD_GOODS_FURNITURE_AND_FURNISHINGS'
            '&sectors=TEXTILES_INTERIOR_TEXTILES_AND_CARPETS'
        )
    ),
    (
        'ENERGY',
        (
            '?sectors=OIL_AND_GAS'
            '&sectors=RENEWABLE_ENERGY'
            '&sectors=POWER'
            '&sectors=WATER'
        )
    ),
    (
        'LIFE_SCIENCES_AND_HEALTHCARE',
        (
            '?sectors=BIOTECHNOLOGY_AND_PHARMACEUTICALS'
            '&sectors=HEALTHCARE_AND_MEDICAL'
        )
    ),
    (
        'TECHNOLOGY',
        (
            '?sectors=COMMUNICATIONS'
            '&sectors=ELECTRONICS_AND_IT_HARDWARE'
            '&sectors=SOFTWARE_AND_COMPUTER_SERVICES'
        ),
    ),
    (
        'INFRASTRUCTURE',
        (
            '?sectors=AIRPORTS'
            '&sectors=CONSTRUCTION'
            '&sectors=LEISURE_AND_TOURISM'
            '&sectors=MARINE'
            '&sectors=PORTS_AND_LOGISTICS'
            '&sectors=RAILWAYS'
        )
    ),
    (
        'PROFESSIONAL_SERVIVES',
        (
            '?sectors=BUSINESS_AND_CONSUMER_SERVICES'
            '&sectors=EDUCATION_AND_TRAINING'
            '&sectors=FINANCIAL_AND_PROFESSIONAL_SERVICES'
        )
    ),
    (
        'CYBER_SECURITY',
        (
            '?sectors=COMMUNICATIONS'
            '&sectors=ELECTRONICS_AND_IT_HARDWARE'
            '&sectors=SECURITY'
            '&sectors=SOFTWARE_AND_COMPUTER_SERVICES'
        )
    ),
    (
        'BIO_ECONOMY',
        (
            '?sectors=AGRICULTURE_HORTICULTURE_AND_FISHERIES'
            '&sectors=CHEMICALS'
        )
    ),
    (
        'SMART_CITIES',
        (
            '?sectors=ELECTRONICS_AND_IT_HARDWARE'
            '&sectors=SOFTWARE_AND_COMPUTER_SERVICES'
        )
    ),
])
def test_search_url_handles_company_classification(filter_value, expected):
    value = company_tags.search_url(filter_value)

    assert value == reverse('company-search') + expected
