from collections import OrderedDict
import itertools
import urllib.parse

from directory_constants.sectors import CONFLATED

from django import template
from django.core.urlresolvers import reverse


register = template.Library()


@register.simple_tag
def search_url(sector_value=None, term=None):
    if isinstance(sector_value, str):
        sector_value = [sector_value]

    params = OrderedDict()

    if sector_value:
        sectors = [CONFLATED.get(item, {item}) for item in sector_value]
        params['sectors'] = list(itertools.chain(*sectors))
    if term:
        params['term'] = term
    querystring = urllib.parse.urlencode(params, doseq=True)
    return reverse('find-a-supplier:search') + '?' + querystring
