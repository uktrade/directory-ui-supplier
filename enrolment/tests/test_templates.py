from django.template.loader import render_to_string

from core import forms


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


def test_robots(rf):
    request = rf.get('/')

    context = {
        'request': request,
    }

    html = render_to_string('robots.txt', context)

    assert 'Sitemap: http://testserver/sitemap.xml' in html


def test_utm_cookie_domain():
    context = {
        'analytics': {
            'UTM_COOKIE_DOMAIN': '.thing.com',
        }
    }
    html = render_to_string('enrolment-base.html', context)

    assert '<meta id="utmCookieDomain" value=".thing.com" />' in html


def test_lead_generation_form():
    context = {
        'form': forms.LeadGenerationForm()
    }
    html = render_to_string('lead-generation.html', context)

    assert html
