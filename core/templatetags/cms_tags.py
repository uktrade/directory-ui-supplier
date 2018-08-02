import re

from bs4 import BeautifulSoup

from django import template

from directory_components.templatetags import directory_components_tags


register = template.Library()


@register.filter
def table_of_contents(value):
    soup = BeautifulSoup(value, 'html.parser')
    return [
        (
            directory_components_tags.build_anchor_id(element, '-section'),
            directory_components_tags.get_label(element)
        )
        for element in soup.findAll('h2')
    ]


@register.filter
def first_paragraph(value):
    soup = BeautifulSoup(value, 'html.parser')
    element = soup.find('p')
    return str(element)


@register.filter
def grouper(value, n):
    ungrouped = value or []
    return [ungrouped[x:x+n] for x in range(0, len(ungrouped), n)]


@register.filter
def add_href_target(value, request):
    soup = BeautifulSoup(value, 'html.parser')
    for element in soup.findAll('a', attrs={'href': re.compile("^http")}):
        if request.META['HTTP_HOST'] not in element.attrs['href']:
            element.attrs['target'] = '_blank'
    return str(soup)
