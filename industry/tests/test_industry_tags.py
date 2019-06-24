from django.core.urlresolvers import reverse

from industry.templatetags import industry_tags


def test_search_url():
    search_url = industry_tags.search_url(
        sector_value='AEROSPACE',
        term='test',
    )

    assert search_url == (
        reverse('find-a-supplier:search') +
        '?industries=AEROSPACE&term=test'
    )
