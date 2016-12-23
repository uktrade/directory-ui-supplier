import os
from unittest.mock import Mock

from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string


supplier_context = {
    'supplier': {
        'mobile': '00000000011',
        'email': 'email@example.com',
    }
}


def test_form_wrapper_next_button():
    context = {
        'wizard': {
            'steps':
                {
                    'step1': 2,
                    'count': 3,
                }
        }
    }
    html = render_to_string('form-wrapper.html', context)
    assert 'value="Next"' in html
    assert 'value="Register"' not in html


def test_form_wrapper_finish_button():
    context = {
        'wizard': {
            'steps':
                {
                    'step1': 3,
                    'count': 3,
                }
        }
    }
    html = render_to_string('form-wrapper.html', context)
    assert 'value="Next"' not in html
    assert 'value="Register"' in html


def test_google_tag_manager():
    expected_head = render_to_string('google_tag_manager_head.html')
    expected_body = render_to_string('google_tag_manager_body.html')

    html = render_to_string('govuk_layout.html')

    assert expected_head in html
    assert expected_body in html
    # sanity check
    assert 'www.googletagmanager.com' in expected_head
    assert 'www.googletagmanager.com' in expected_body


def test_international_landing_page_sector_feature_flag_enabled():
    context = {
        'features': {
            'FEATURE_SECTOR_LANDING_PAGES_ENABLED': True
        }
    }
    html = render_to_string('landing-page-international.html', context)

    assert reverse('international-sector-list') in html


def test_international_landing_page_sector_feature_flag_disabled():
    context = {
        'features': {
            'FEATURE_SECTOR_LANDING_PAGES_ENABLED': False
        }
    }
    html = render_to_string('landing-page-international.html', context)

    assert reverse('international-sector-list') not in html


def test_templates_render_successfully():

    template_list = []
    template_dirs = [
        os.path.join(settings.BASE_DIR, 'enrolment/templates'),
        os.path.join(settings.BASE_DIR, 'supplier/templates'),
    ]
    for template_dir in template_dirs:
        for dir, dirnames, filenames in os.walk(template_dir):
            for filename in filenames:
                path = os.path.join(dir, filename).replace(template_dir, '')
                template_list.append(path.lstrip('/'))

    default_context = {
        'supplier': None,
        'form': Mock(),
    }
    assert template_list
    for template in template_list:
        render_to_string(template, default_context)
