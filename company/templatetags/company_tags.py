from collections import OrderedDict
from datetime import datetime
from dateutil.relativedelta import relativedelta
import urllib.parse

from django import template
from django.core.paginator import EmptyPage
from django.core.urlresolvers import reverse

from enrolment.constants import SECTOR_FILTER_GROUPS


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


@register.simple_tag
def search_url(sector_value=None, term=None):
    params = OrderedDict()
    if sector_value:
        sectors = SECTOR_FILTER_GROUPS.get(sector_value, {sector_value})
        params['sectors'] = sectors
    if term:
        params['term'] = term
    querystring = urllib.parse.urlencode(params, doseq=True)
    return reverse('company-search') + '?' + querystring


@register.simple_tag(takes_context=True)
def pagination_querystring_previous(context):
    data = {**context['form'].cleaned_data}
    try:
        data['page'] = context['pagination'].previous_page_number()
    except EmptyPage:
        pass
    return urllib.parse.urlencode(data, doseq=True)


@register.simple_tag(takes_context=True)
def pagination_querystring_next(context):
    params = context['form'].cleaned_data
    page = context['pagination'].next_page_number()
    return urllib.parse.urlencode({**params, 'page': page}, doseq=True)
