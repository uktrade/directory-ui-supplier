from datetime import datetime

from freezegun import freeze_time

from enrolment.templatetags import date_recency


@freeze_time()
def test_date_recency_hours():
    value = datetime.utcnow() - timedelta(hours=23)

    assert date_recency(value) == 'Updated 23 hours ago'


@freeze_time()
def test_date_recency_days():
    pass


@freeze_time()
def test_date_recency_months():
    pass


@freeze_time()
def test_date_recency_years():
    pass
