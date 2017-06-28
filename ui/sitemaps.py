from django.contrib import sitemaps
from django.core.urlresolvers import reverse

from enrolment import views


class SectorLandingPageSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        pages = views.SectorDetailView.get_active_pages()
        return list(pages.keys())

    def location(self, item):
        return reverse('sector-detail-summary', kwargs={'slug': item})


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
