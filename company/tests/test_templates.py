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
        'summary': '',
        'slug': 'uk-exporting-co-ltd'
    }
}

NO_RESULTS_FOUND_LABEL = 'No companies found'
CONTACT_COMPANY_LABEL = 'Contact company'
EMAIL_COMPANY_LABEL = 'Email company'
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

    assert 'Updated: 1 hour ago' in html


def test_company_public_profile_list_link_to_profle():
    context = {
        'companies': [
            default_context['company']
        ]
    }
    url = reverse(
        'public-company-profiles-detail',
        kwargs={
            'company_number': default_context['company']['number'],
            'slug': default_context['company']['slug'],
        }
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


def test_company_public_profile_results_summary():
    company = {
        **default_context['company'],
        'summary': (
            'summary summary summary summary summary summary summary '
            'summary summary summary summary summary summary summary '
            'summary summary summary summary summary summary summary'
        )
    }

    context = {
        'companies': [company],
    }
    html = render_to_string('company-public-profile-list.html', context)
    expected = (
        'summary summary summary summary summary summary summary summary '
        'summary summary summary summary summary summary summary summary '
        'summ...'
    )

    assert expected in html


def test_company_public_profile_results_description():
    company = {
        **default_context['company'],
        'description': (
            'description description description description description '
            'description description description description description '
            'description description description description description '
            'description description description description description '
            'description'
        ),
        'summary': '',
    }

    context = {
        'companies': [company],
    }
    html = render_to_string('company-public-profile-list.html', context)
    expected = (
        'description description description description description '
        'description description description description description '
        'description ...'
    )

    assert expected in html


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
        'companies': [
            {'number': '01234567A', 'slug': 'hello'},
            {'number': '01234567B', 'slug': 'hello'}
        ],
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
        'companies': [
            {'number': '01234567A', 'slug': 'hello'},
            {'number': '01234567B', 'slug': 'hello'}
        ],
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
        'companies': [
            {'number': '01234567B', 'slug': 'hello'}
        ],
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
        'companies': [
            {'number': '01234567A', 'slug': 'hello'},
            {'number': '01234567B', 'slug': 'hello'}
        ],
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
        'companies': [
            {'number': '01234567A', 'slug': 'hello'},
        ],
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
        'companies': [
            {'number': '01234567A', 'slug': 'hello'},
            {'number': '01234567B', 'slug': 'hello'}
        ],
        'show_companies_count': False,
    }

    html = render_to_string('company-public-profile-list.html', context)

    assert 'Displaying 2  companies' in html


def test_case_study_detail_report_button():
    context = {
        'case_study': {
            'company': {
                'number': '012344',
                'slug': 'hello',
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
            'supplier_case_studies': [],
            'slug': 'hello',
        }
    }
    html = render_to_string('company-profile-detail.html', context)

    assert RECENT_PROJECTS_LABEL not in html


def test_profile_case_studies_present():
    context = {
        'company': {
            'number': '012344',
            'supplier_case_studies': [{'pk': 1, 'slug': 'hello'}],
            'slug': 'hello'
        }
    }
    html = render_to_string('company-profile-detail.html', context)

    assert RECENT_PROJECTS_LABEL in html


def test_public_profile_contact_button():
    context = {
        'company': default_context['company'],
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


def test_public_profile_sectors_link_feature_flag_off():
    context = {
        'features': {
            'FEATURE_SEARCH_FILTER_SECTOR_ENABLED': False
        },
        **default_context
    }
    html = render_to_string('company-profile-detail.html', context)
    url = reverse('public-company-profiles-list') + '?sectors=SECTOR1'

    assert url in html


def test_public_profile_sectors_link_feature_flag_on():
    context = {
        'features': {
            'FEATURE_SEARCH_FILTER_SECTOR_ENABLED': True
        },
        **default_context
    }
    html = render_to_string('company-profile-detail.html', context)

    assert reverse('company-search') + '?sector=SECTOR1' in html


def test_public_profile_report_button():
    context = {
        'company': {
            'number': '012344',
            'slug': 'hello',
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
            'description': 'the description!',
            'slug': 'hello',
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
            'description': 'the description!',
            'slug': 'hello',
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
            'description': description,
            'slug': 'hello',
        }
    }
    html = render_to_string('company-profile-detail.html', context)

    assert expected in html


def test_company_contact_displays_company_name():
    html = render_to_string('company-contact-form.html', default_context)
    assert default_context['company']['name'] in html


def test_company_contact_displays_cancel_link():
    html = render_to_string('company-contact-form.html', default_context)
    url = reverse(
        'public-company-profiles-detail',
        kwargs={
            'company_number': default_context['company']['number'],
            'slug': default_context['company']['slug'],
        }
    )

    assert url in html


def test_contact_company_success():
    html = render_to_string('company-contact-success.html', default_context)

    assert 'Your message has been sent to UK exporting co ltd.' in html
    assert "/suppliers/123456/contact/sent" in html


def test_case_study_contact_button():
    context = {
        'case_study': {
            'company': default_context['company'],
        },
    }
    html = render_to_string('supplier-case-study-detail.html', context)
    expected_url = reverse(
        'contact-company', kwargs={'company_number': '123456'}
    )

    assert EMAIL_COMPANY_LABEL in html
    assert default_context['company']['email_address'] not in html
    assert expected_url in html


def test_case_study_handles_not_present_image_one():
    context = {
        'case_study': {
            'company': default_context['company'],
            'image_one': None
        }
    }
    html = render_to_string('supplier-case-study-detail.html', context)

    assert 'None' not in html


def test_company_profile_details_renders_keywords():
    template_name = 'company-profile-detail.html'
    html = render_to_string(template_name, default_context)

    assert default_context['company']['keywords']
    for keyword in default_context['company']['keywords']:
        assert keyword in html
