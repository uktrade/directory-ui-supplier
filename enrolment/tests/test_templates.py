import os
from unittest.mock import Mock

from django.conf import settings
from django.template.loader import render_to_string


supplier_context = {
    'supplier': {
        'mobile': '00000000011',
        'email': 'email@example.com',
    }
}


def test_google_tag_manager():
    expected_head = render_to_string('google_tag_manager_head.html')
    expected_body = render_to_string('google_tag_manager_body.html')

    html = render_to_string('govuk_layout.html')

    assert expected_head in html
    assert expected_body in html
    # sanity check
    assert 'www.googletagmanager.com' in expected_head
    assert 'www.googletagmanager.com' in expected_body


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


def test_footer_contact_us(rf):
    context = {
        'request': rf.get('/creative')
    }
    html = render_to_string('footer.html', context)
    href = (
        'href="mailto:help@digital.trade.gov.uk?subject=General'
        '%20enquiry%20for%20/creative'
    )

    assert href in html


def test_social_share_all_populated():
    context = {
        'social': {
            'image': 'image.png',
            'title': 'a title',
            'description': 'a description',
        }
    }
    html = render_to_string('social.html', context)

    assert '<meta property="og:type" content="website" />' in html
    assert '<meta property="og:image" content="image.png" />' in html
    assert '<meta property="og:title" content="a title" />'in html
    assert '<meta property="og:description" content="a description" />' in html


def test_social_share_not_populated():
    context = {}
    html = render_to_string('social.html', context)
    url = '/static/govuk-0.18.0/assets/images/opengraph-image.f86f1d0dd106.png'

    assert '<meta property="og:type" content="website" />' in html
    assert '<meta property="og:image" content="{0}" />'.format(url) in html
    assert '<meta property="og:title"' not in html
    assert '<meta property="og:description"' not in html
