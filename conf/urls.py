from django.conf import settings
from django.conf.urls import url
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from django.views.static import serve

import core.views
import company.views
import industry.views
import notifications.views
import conf.sitemaps

sitemaps = {
    'static': conf.sitemaps.StaticViewSitemap,
    'industries': conf.sitemaps.SectorLandingPageSitemap,
}

urlpatterns = [
    url(
        r"^sitemap\.xml$", sitemap, {'sitemaps': sitemaps},
        name='sitemap'
    ),
    url(
        r"^robots\.txt$",
        TemplateView.as_view(
            template_name='robots.txt', content_type='text/plain'
        ),
        name='robots'
    ),
    url(
        r"^$",
        core.views.LandingPageCMSView.as_view(),
        name="index"
    ),
    url(
        r'^suppliers/$',
        company.views.PublishedProfileListView.as_view(),
        name='public-company-profiles-list',
    ),
    url(
        r'^search/$',
        company.views.CompanySearchView.as_view(),
        name='company-search',
    ),
    url(
        r'^suppliers/(?P<company_number>[a-zA-Z0-9]+)/contact/$',
        company.views.ContactCompanyView.as_view(),
        name='contact-company',
    ),
    url(
        r'^suppliers/(?P<company_number>[a-zA-Z0-9]+)/(?P<slug>.+)/$',
        company.views.PublishedProfileDetailView.as_view(),
        name='public-company-profiles-detail',
    ),
    url(
        r'^industries/$',
        industry.views.IndustryLandingPageCMSView.as_view(),
        name='sector-list',
    ),
    url(
        r'^industries/contact/(?P<slug>[\w-]+)/$',
        industry.views.IndustryDetailContactCMSView.as_view(),
        name='sector-detail-cms-contact',
    ),
    url(
        r'^industries/contact/$',
        industry.views.IndustryLandingPageContactCMSView.as_view(),
        name='sector-list-cms-contact',
    ),
    url(
        r'^industry-articles/(?P<slug>[\w-]+)/$',
        industry.views.IndustryArticleCMSView.as_view(),
        name='sector-article',
    ),
    url(
        r'^industries/(?P<slug>.+)/$',
        industry.views.IndustryDetailCMSView.as_view(),
        name='sector-detail-verbose',
    ),
    url(
        r'^case-study/(?P<id>.+)/(?P<slug>.+)/$',
        company.views.CaseStudyDetailView.as_view(),
        name='case-study-details'
    ),
    url(
        r'^subscribe/$',
        core.views.AnonymousSubscribeFormView.as_view(),
        name='subscribe'
    ),
    url(
        r'^feedback/$',
        core.views.LeadGenerationFormView.as_view(),
        name='lead-generation'
    ),
    url(
        r'^unsubscribe/$',
        notifications.views.AnonymousUnsubscribeView.as_view(),
        name='anonymous-unsubscribe'
    ),

    # old export opportunity urls. redirect to CMS industry pages.
    url(
        r'^campaign/food-is-great/.*/$',
        core.views.RedirectToCMSIndustryView.as_view(),
        {'slug': 'food-and-drink'},
    ),
    url(
        r'^campaign/legal-is-great/.*/$',
        core.views.RedirectToCMSIndustryView.as_view(),
        {'slug': 'legal'},
    ),
    url(
        r'^export-opportunity/food-is-great/.*/$',
        core.views.RedirectToCMSIndustryView.as_view(),
        {'slug': 'food-and-drink'},
    ),
    url(
        r'^export-opportunity/legal-is-great/.*/$',
        core.views.RedirectToCMSIndustryView.as_view(),
        {'slug': 'legal'},
    ),
    # obsolete. use `sector-detail-verbose`
    url(
        r'^industries/(?P<slug>.+)/summary/$',
        core.views.RedirectToCMSIndustryView.as_view(),
        name='sector-detail-summary',
    ),
    # obsolete. use `case-study-details`
    url(
        r'^case-study/(?P<id>.+)/$',
        company.views.CaseStudyDetailView.as_view(),
        name='case-study-details-slugless'
    ),
    # obsolete. use `public-company-profiles-detail`
    url(
        r'^suppliers/(?P<company_number>[a-zA-Z0-9]+)/$',
        company.views.PublishedProfileDetailView.as_view(),
        name='public-company-profiles-detail-slugless'
    ),
]


if settings.THUMBNAIL_STORAGE_CLASS_NAME == 'local-storage':
    urlpatterns += [
        url(
            r'^media/(?P<path>.*)$',
            serve,
            {'document_root': settings.MEDIA_ROOT}
        ),
    ]
