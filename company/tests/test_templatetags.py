from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

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
