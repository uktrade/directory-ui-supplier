from django.template.loader import render_to_string


supplier_context = {
    'supplier': {
        'mobile': '00000000011',
        'email': 'email@example.com',
    }
}


MESSAGE_ENGLISH_ONLY = 'Page in English only'
MORE_INDUSTRIES_LABEL = 'See more industries'


def test_google_tag_manager_project_id():
    context = {
        'analytics': {
            'GOOGLE_TAG_MANAGER_ID': '1234567',
        }
    }
    head_html = render_to_string('google_tag_manager_head.html', context)
    body_html = render_to_string('google_tag_manager_body.html', context)

    assert '1234567' in head_html
    assert 'https://www.googletagmanager.com/ns.html?id=1234567' in body_html


def test_google_tag_manager():
    context = {}
    expected_head = render_to_string('google_tag_manager_head.html', context)
    expected_body = render_to_string('google_tag_manager_body.html', context)

    html = render_to_string('govuk_layout.html', context)

    assert expected_head in html
    assert expected_body in html
    # sanity check
    assert 'www.googletagmanager.com' in expected_head
    assert 'www.googletagmanager.com' in expected_body


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


def test_language_switcher_show():
    context = {
        'language_switcher': {
            'show': True
        }
    }
    html = render_to_string('language_switcher.html', context)

    assert '<form' in html
    assert MESSAGE_ENGLISH_ONLY not in html


def test_language_switcher_hide():
    context = {
        'language_switcher': {
            'show': False
        },
        'request': {
            'LANGUAGE_CODE': 'en-gb'
        }
    }
    html = render_to_string('language_switcher.html', context)

    assert '<form' not in html
    assert MESSAGE_ENGLISH_ONLY not in html


def test_language_switcher_hide_not_translated_english_selected():
    context = {
        'language_switcher': {
            'show': False
        },
        'request': {
            'LANGUAGE_CODE': 'en-gb'
        }
    }
    html = render_to_string('language_switcher.html', context)

    assert '<form' not in html
    assert MESSAGE_ENGLISH_ONLY not in html


def test_language_switcher_hide_not_translated_german_selected():
    context = {
        'language_switcher': {
            'show': False
        },
        'request': {
            'LANGUAGE_CODE': 'de',
        }
    }
    html = render_to_string('language_switcher.html', context)

    assert '<form' not in html
    assert 'Seite nur auf Englisch' in html


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
    html = render_to_string('govuk_layout.html', context)

    assert '<meta id="utmCookieDomain" value=".thing.com" />' in html


def test_international_landing_page_button_feature_flag_on():
    context = {
        'features': {
            'FEATURE_MORE_INDUSTRIES_BUTTON_ENABLED': True,
        }
    }
    html = render_to_string('landing-page.html', context)

    assert MORE_INDUSTRIES_LABEL in html


def test_international_landing_page_button_feature_flag_off():
    context = {
        'features': {
            'FEATURE_MORE_INDUSTRIES_BUTTON_ENABLED': False,
        }
    }
    html = render_to_string('landing-page.html', context)

    assert MORE_INDUSTRIES_LABEL not in html
