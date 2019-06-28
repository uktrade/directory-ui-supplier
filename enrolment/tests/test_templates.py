from django.template.loader import render_to_string


def test_robots(rf):
    request = rf.get('/')

    context = {
        'request': request,
    }

    html = render_to_string('robots.txt', context)

    assert 'Sitemap: http://testserver/trade/sitemap.xml' in html


def test_utm_cookie_domain():
    context = {
        'directory_components_analytics': {
            'UTM_COOKIE_DOMAIN': '.thing.com',
        }
    }
    html = render_to_string('enrolment-base.html', context)

    assert '<meta id="utmCookieDomain" value=".thing.com" />' in html
