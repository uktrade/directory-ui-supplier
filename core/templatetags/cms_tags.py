import datetime
import re

from bs4 import BeautifulSoup

from django import template
from django.utils.text import slugify


register = template.Library()


def build_anchor_id(element):
    return slugify(get_label(element) + '-section')


def get_label(element):
    return re.sub(r'^.* \- ', '', element.contents[0])


@register.filter
def add_anchors(value):
    soup = BeautifulSoup(value, 'html.parser')
    for element in soup.findAll('h2'):
        element.attrs['id'] = build_anchor_id(element)
    return str(soup)


@register.filter
def table_of_contents(value):
    soup = BeautifulSoup(value, 'html.parser')
    return [
        (build_anchor_id(element), get_label(element))
        for element in soup.findAll('h2')
    ]


@register.filter
def first_paragraph(value):
    soup = BeautifulSoup(value, 'html.parser')
    element = soup.find('p')
    return str(element)


@register.filter
def first_image(value):
    soup = BeautifulSoup(value, 'html.parser')
    element = soup.find('img')
    if not element:
        return ''
    del element['height']
    return element


@register.filter
def to_date(value):
    return datetime.datetime.strptime(value, '%Y-%m-%d')


@register.filter
def chunk_list(value, length):
    unchunked  = value or []
    return [unchunked[x:x+length] for x in range(0, len(unchunked), length)]
