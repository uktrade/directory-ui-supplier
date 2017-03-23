from datetime import datetime
from dateutil.relativedelta import relativedelta

from django import template

register = template.Library()


@register.filter
def date_recency(value):
    if not value:
        return ''
    now = datetime.utcnow()
    delta = relativedelta(now, value)
    if value >= now - relativedelta(days=1):
        template = '{delta.hours} hour{hours_suffix} ago'
    elif value >= now - relativedelta(months=1):
        template = '{delta.days} day{days_suffix} ago'
    elif value >= now - relativedelta(years=1):
        template = '{delta.months} month{months_suffix} ago'
    else:
        template = (
            '{delta.years} year{years_suffix} and '
            '{delta.months} month{months_suffix} ago'
        )
    return template.format(
        delta=delta,
        hours_suffix='s' if delta.hours > 1 else '',
        days_suffix='s' if delta.days > 1 else '',
        months_suffix='s' if delta.months > 1 else '',
        years_suffix='s' if delta.years > 1 else '',
    )
