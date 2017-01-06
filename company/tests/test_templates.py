from datetime import datetime, timedelta

from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.template.loader import render_to_string

from company import forms


default_context = {
    'company': {
        'sectors': [
            {'value': 'SECTOR1', 'label': 'sector 1'},
            {'value': 'SECTOR2', 'label': 'sector 2'},
        ],
        'number': '123456',
        'name': 'UK exporting co ltd.',
        'description': 'Exporters of UK wares.',
        'website': 'www.ukexportersnow.co.uk',
        'logo': 'www.ukexportersnow.co.uk/logo.png',
        'keywords': 'word1 word2',
        'date_of_creation': '2 Mar 2015',
        'modified': datetime.now() - timedelta(hours=1),
        'contact_details': {
            'email_address': 'sales@example.com',
        },
    }
}

NO_RESULTS_FOUND_LABEL = 'No companies found'


def test_company_public_profile_list_link_to_profle():
    context = {
        'companies': [
            default_context['company']
        ]
    }
    url = reverse(
        'public-company-profiles-detail',
        kwargs={'company_number': default_context['company']['number']}
    )
    html = render_to_string('company-public-profile-list.html', context)

    assert 'href="{url}"'.format(url=url) in html


def test_company_public_profile_no_results_label():
    form = forms.PublicProfileSearchForm(data={'sectors': 'WATER'})
    assert form.is_valid()
    context = {
        'companies': [],
        'form': form,
    }
    html = render_to_string('company-public-profile-list.html', context)

    assert NO_RESULTS_FOUND_LABEL in html


def test_company_public_profile_results_label():
    form = forms.PublicProfileSearchForm(data={'sectors': 'WATER'})
    assert form.is_valid()
    paginator = Paginator([{}], 10)
    context = {
        'selected_sector_label': 'thing',
        'companies':  [
            default_context['company']
        ],
        'pagination': paginator.page(1),
        'form': form,
    }
    html = render_to_string('company-public-profile-list.html', context)
    assert "Displaying 1 of 1 \'thing\' company" in html
    assert NO_RESULTS_FOUND_LABEL not in html


def test_company_public_profile_results_label_plural():
    form = forms.PublicProfileSearchForm(data={'sectors': 'WATER'})
    assert form.is_valid()
    paginator = Paginator(range(10), 10)
    context = {
        'selected_sector_label': 'thing',
        'companies': [
            default_context['company'],
            default_context['company'],
        ],
        'pagination': paginator.page(1),
        'form': form,
    }
    html = render_to_string('company-public-profile-list.html', context)
    assert "Displaying 2 of 10 \'thing\' companies" in html
    assert NO_RESULTS_FOUND_LABEL not in html


def test_company_public_profile_list_paginate_next():
    form = forms.PublicProfileSearchForm(data={'sectors': 'WATER'})
    assert form.is_valid()

    paginator = Paginator(range(100), 10)
    context = {
        'pagination': paginator.page(1),
        'form': form,
        'companies': [{'number': '01234567A'}]
    }

    html = render_to_string('company-public-profile-list.html', context)

    assert 'href="?sectors=WATER&page=2"' in html


def test_company_public_profile_list_paginate_prev():
    form = forms.PublicProfileSearchForm(data={'sectors': 'WATER'})
    assert form.is_valid()

    paginator = Paginator(range(100), 10)
    context = {
        'pagination': paginator.page(2),
        'form': form,
        'companies': [{'number': '01234567A'}]
    }

    html = render_to_string('company-public-profile-list.html', context)

    assert 'href="?sectors=WATER&page=1"' in html


def test_public_profile_verbose():
    context = {
        'show_description': True,
        'company': {
            'summary': 'the summary!',
            'description': 'the description!'
        }
    }
    html = render_to_string('company-profile-detail.html', context)

    assert 'href="?verbose=true"' not in html
    assert context['company']['summary'] not in html
    assert context['company']['description'] in html


def test_public_profile_non_verbose():
    context = {
        'show_description': False,
        'company': {
            'summary': 'the summary!',
            'description': 'the description!'
        }
    }
    html = render_to_string('company-profile-detail.html', context)

    assert 'href="?verbose=true"' in html
    assert context['company']['summary'] in html
    assert context['company']['description'] not in html
