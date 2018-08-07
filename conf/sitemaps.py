from directory_cms_client.client import cms_api_client
import directory_cms_client.constants

from django.contrib import sitemaps
from django.core.urlresolvers import reverse

from core import helpers


class SectorLandingPageSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        response = cms_api_client.list_by_page_type(
            directory_cms_client.constants.FIND_A_SUPPLIER_INDUSTRY_TYPE
        )
        pages = helpers.handle_cms_response(response)['items']
        return [page['meta']['slug'] for page in pages]

    def location(self, item):
        return reverse('sector-detail-verbose', kwargs={'slug': item})


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return [
            'index',
            'public-company-profiles-list',
            'sector-list',
            'subscribe',
        ]

    def location(self, item):
        return reverse(item)
