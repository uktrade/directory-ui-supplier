from datetime import datetime, timedelta

from django import template

register = template.Library()


@register.filter
def date_recency(value):
    now = datetime.utcnow()
    delta = now - value
    if value >= now - timedelta(days=1):
        return 'Updated {hours} hours ago'.format(hours=delta.hours)
    if value >= now - timedelta(months=1):
        return 'Updated {days} days ago'.format(days=delta.days)
    if value >= now - timedelta(years=1):
        return 'Updated {months} months ago'.format(months=delta.months)
    if value >= now - timedelta(years=1):
        return 'Updated {years} and {months} months ago'.format(
            years=delta.years
            months=delta.months - (delta.years * 12)
        )
