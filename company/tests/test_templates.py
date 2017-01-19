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
        'date_of_creation': datetime(2015, 3, 2),
        'modified': datetime.now() - timedelta(hours=1),
        'email_address': 'sales@example.com',
    }
}

NO_RESULTS_FOUND_LABEL = 'No companies found'
CONTACT_COMPANY_LABEL = 'Contact company'
RECENT_PROJECTS_LABEL = 'Recent projects'


def test_company_public_profile_list_date_of_creation():
    context = {
        'companies': [
            default_context['company']
        ]
    }
    html = render_to_string('company-public-profile-list.html', context)

    assert '2015' in html


def test_company_public_profile_list_modified():
    context = {
        'companies': [
            default_context['company']
        ]
    }

    html = render_to_string('company-public-profile-list.html', context)

    assert 'Updated an hour ago' in html


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
        'show_companies_count': True,
    }
    html = render_to_string('company-public-profile-list.html', context)

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
        'show_companies_count': True,
    }
    html = render_to_string('company-public-profile-list.html', context)

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


def test_company_public_profile_list_paginate_label_single_with_sector():
    form = forms.PublicProfileSearchForm(data={'sectors': 'WATER'})
    assert form.is_valid()

    paginator = Paginator(range(100), 10)
    context = {
        'pagination': paginator.page(2),
        'form': form,
        'companies': [{'number': '01234567A'}],
        'show_companies_count': True,
        'selected_sector_label': 'Water',
    }

    html = render_to_string('company-public-profile-list.html', context)

    assert 'Displaying 1 of 100 Water companies' in html


def test_company_public_profile_list_paginate_label_multiple_with_sector():
    form = forms.PublicProfileSearchForm(data={'sectors': 'WATER'})
    assert form.is_valid()

    paginator = Paginator(range(100), 10)
    context = {
        'pagination': paginator.page(2),
        'form': form,
        'companies': [{'number': '01234567A'}, {'number': '01234567B'}],
        'show_companies_count': True,
        'selected_sector_label': 'Water',
    }

    html = render_to_string('company-public-profile-list.html', context)

    assert 'Displaying 2 of 100 Water companies' in html


def test_company_public_profile_list_paginate_label_single_without_sector():
    form = forms.PublicProfileSearchForm(data={})
    assert form.is_valid()

    paginator = Paginator(range(100), 10)
    context = {
        'pagination': paginator.page(2),
        'form': form,
        'companies': [{'number': '01234567A'}],
        'show_companies_count': False,
    }

    html = render_to_string('company-public-profile-list.html', context)

    assert 'Displaying 1  company' in html


def test_company_public_profile_list_paginate_label_multiple_without_sector():
    form = forms.PublicProfileSearchForm(data={})
    assert form.is_valid()

    paginator = Paginator(range(100), 10)
    context = {
        'pagination': paginator.page(2),
        'form': form,
        'companies': [{'number': '01234567A'}, {'number': '01234567B'}],
        'show_companies_count': False,
    }

    html = render_to_string('company-public-profile-list.html', context)

    assert 'Displaying 2  companies' in html


def test_case_study_detail_report_button():
    context = {
        'case_study': {
            'company': {
                'number': '012344',
            }
        }
    }
    html = render_to_string('supplier-case-study-detail.html', context)
    href = "mailto:help@digital.trade.gov.uk?subject=Report%20profile%20012344"

    assert href in html


def test_profile_case_studies_empty():
    context = {
        'company': {
            'number': '012344',
            'supplier_case_studies': []
        }
    }
    html = render_to_string('company-profile-detail.html', context)

    assert RECENT_PROJECTS_LABEL not in html


def test_profile_case_studies_present():
    context = {
        'company': {
            'number': '012344',
            'supplier_case_studies': [{'pk': 1}]
        }
    }
    html = render_to_string('company-profile-detail.html', context)

    assert RECENT_PROJECTS_LABEL in html


def test_public_profile_contact_button_feature_flag_off(settings):
    context = {
        'company': default_context['company'],
        'features': {
            'FEATURE_CONTACT_COMPANY_FORM_ENABLED': False,
        }
    }
    html = render_to_string('company-profile-detail.html', context)
    expected_url = reverse(
        'contact-company', kwargs={'company_number': '123456'}
    )

    assert CONTACT_COMPANY_LABEL in html
    assert html.count(default_context['company']['email_address']) == 2
    assert html.count(expected_url) == 0


def test_public_profile_contact_button_feature_flag_on(settings):
    context = {
        'company': default_context['company'],
        'features': {
            'FEATURE_CONTACT_COMPANY_FORM_ENABLED': True,
        }
    }
    html = render_to_string('company-profile-detail.html', context)
    expected_url = reverse(
        'contact-company', kwargs={'company_number': '123456'}
    )

    assert CONTACT_COMPANY_LABEL in html
    assert html.count(default_context['company']['email_address']) == 0
    assert html.count(expected_url) == 2


def test_public_profile_contact_button_no_email():
    html = render_to_string('company-profile-detail.html', {})

    assert CONTACT_COMPANY_LABEL not in html


def test_public_profile_report_button():
    context = {
        'company': {
            'number': '012344',
        }
    }
    html = render_to_string('company-profile-detail.html', context)
    href = "mailto:help@digital.trade.gov.uk?subject=Report%20profile%20012344"

    assert href in html


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


def test_public_profile_non_verbose_missing_summary():
    description = (
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed doesel '
        'eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enime'
        ' ad minim veniam, quis nostrud exercitation ullamco laboris nisileds'
    )
    expected = description[0:197] + '...'
    # sanity testing the values for the test. The description should be
    # truncated to 200 chars, including the ellipsis chars.
    assert len(description) == 204
    assert len(expected) == 200

    context = {
        'show_description': False,
        'company': {
            'summary': '',
            'description': description
        }
    }
    html = render_to_string('company-profile-detail.html', context)

    assert expected in html
