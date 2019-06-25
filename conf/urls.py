import directory_components.views
import directory_healthcheck.views
from directory_components.decorators import skip_ga360

from django.conf import settings
from django.conf.urls import include, url
from django.contrib.sitemaps.views import sitemap
from django.views.static import serve
from django.views.generic import RedirectView

from directory_constants import slugs

import core.views
import find_a_supplier.views
import industry.views
import investment_support_directory.views
import notifications.views
import conf.sitemaps


sitemaps = {
    'static': conf.sitemaps.StaticViewSitemap,
    'industries': conf.sitemaps.SectorLandingPageSitemap,
}

healthcheck_urls = [
    url(
        r'^$',
        skip_ga360(directory_healthcheck.views.HealthcheckView.as_view()),
        name='healthcheck'
    ),
]


investment_support_directory_urls = [
    url(
        r'^$',
        investment_support_directory.views.HomeView.as_view(),
        name='home'
    ),
    url(
        r'^search/$',
        investment_support_directory.views.CompanySearchView.as_view(),
        name='search'
    ),
    url(
        r'^(?P<company_number>[a-zA-Z0-9]+)/contact/$',
        investment_support_directory.views.ContactView.as_view(),
        name='company-contact',
    ),
    url(
        r'^(?P<company_number>[a-zA-Z0-9]+)/sent/$',
        investment_support_directory.views.ContactSuccessView.as_view(),
        name='company-contact-sent',
    ),
    url(
        r'^(?P<company_number>[a-zA-Z0-9]+)/(?P<slug>.+)/$',
        investment_support_directory.views.ProfileView.as_view(),
        name='profile'
    ),
    url(
        r'^(?P<company_number>[a-zA-Z0-9]+)/$',
        investment_support_directory.views.ProfileView.as_view(),
        name='profile-slugless'
    ),
]


find_a_supplier_urls = [
    url(
        r'^search/$',
        find_a_supplier.views.CompanySearchView.as_view(),
        name='search',
    ),
    url(
        r'^suppliers/$',
        find_a_supplier.views.PublishedProfileListView.as_view(),
        name='public-company-profiles-list',
    ),
    url(
        r'^suppliers/(?P<company_number>[a-zA-Z0-9]+)/contact/$',
        find_a_supplier.views.ContactCompanyView.as_view(),
        name='company-contact',
    ),
    url(
        r'^suppliers/(?P<company_number>[a-zA-Z0-9]+)/contact/success/$',
        find_a_supplier.views.ContactCompanySentView.as_view(),
        name='company-contact-sent',
    ),
    url(
        r'^suppliers/(?P<company_number>[a-zA-Z0-9]+)/(?P<slug>.+)/$',
        find_a_supplier.views.ProfileView.as_view(),
        name='profile',
    ),
    # obsolete. use `find-a-supplier:profile`
    url(
        r'^suppliers/(?P<company_number>[a-zA-Z0-9]+)/$',
        find_a_supplier.views.ProfileView.as_view(),
        name='profile-slugless'
    ),
]

urlpatterns = [
    url(
        r'^healthcheck/',
        include(
            healthcheck_urls, namespace='healthcheck', app_name='healthcheck'
        )
    ),
    url(
        r"^sitemap\.xml$", skip_ga360(sitemap), {'sitemaps': sitemaps},
        name='sitemap'
    ),
    url(
        r"^robots\.txt$",
        skip_ga360(directory_components.views.RobotsView.as_view()),
        name='robots'
    ),
    url(
        r"^$",
        core.views.LandingPageCMSView.as_view(),
        name="index"
    ),

    url(
        r'^industries/$',
        industry.views.IndustryLandingPageCMSView.as_view(),
        name='sector-list',
    ),
    url(
        r'^industries/contact/sent/$',
        industry.views.IndustryLandingPageContactCMSSentView.as_view(),
        {'slug': slugs.FIND_A_SUPPLIER_INDUSTRY_CONTACT},
        name='sector-list-cms-contact-sent',
    ),
    url(
        r'^industries/contact/(?P<slug>[\w-]+)/sent/$',
        industry.views.IndustryDetailContactCMSSentView.as_view(),
        name='sector-detail-cms-contact-sent',
    ),
    url(
        r'^industries/contact/(?P<slug>[\w-]+)/$',
        industry.views.IndustryDetailContactCMSView.as_view(),
        name='sector-detail-cms-contact',
    ),
    url(
        r'^industries/contact/$',
        industry.views.IndustryLandingPageContactCMSView.as_view(),
        {'slug': slugs.FIND_A_SUPPLIER_INDUSTRY_CONTACT},
        name='sector-list-cms-contact',
    ),
    url(
        r'^industry-articles/(?P<slug>[\w-]+)/$',
        industry.views.IndustryArticleCMSView.as_view(),
        name='sector-article',
    ),
    url(
        r'^industries/creative/$',
        core.views.RedirectToCMSIndustryView.as_view(),
        {'slug': 'creative-services'},
    ),
    url(
        r'^industries/health/$',
        core.views.RedirectToCMSIndustryView.as_view(),
        {'slug': 'healthcare'},
    ),
    url(
        r'^industries/legal/$',
        core.views.RedirectToCMSIndustryView.as_view(),
        {'slug': 'legal-services'},
    ),
    url(
        r'^industries/tech/$',
        core.views.RedirectToCMSIndustryView.as_view(),
        {'slug': 'technology'},
    ),
    url(
        r'^industries/(?P<slug>.+)/$',
        industry.views.IndustryDetailCMSView.as_view(),
        name='sector-detail-verbose',
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
    url(
        r'^case-study/(?P<id>.+)/(?P<slug>.+)/$',
        find_a_supplier.views.CaseStudyDetailView.as_view(),
        name='case-study-details'
    ),
    # obsolete. use `case-study-details`
    url(
        r'^case-study/(?P<id>.+)/$',
        find_a_supplier.views.CaseStudyDetailView.as_view(),
        name='case-study-details-slugless'
    ),
    # obsolete. use `sector-detail-verbose`
    url(
        r'^industries/(?P<slug>.+)/summary/$',
        core.views.RedirectToCMSIndustryView.as_view(),
        name='sector-detail-summary',
    ),
    url(
        r'^',
        include(find_a_supplier_urls, namespace='find-a-supplier'),
    )
]

if settings.THUMBNAIL_STORAGE_CLASS_NAME == 'local-storage':
    urlpatterns += [
        url(
            r'^media/(?P<path>.*)$',
            skip_ga360(serve),
            {'document_root': settings.MEDIA_ROOT}
        ),
    ]


urlpatterns = [
    url(
        r'^trade/',
        include(urlpatterns)
    ),
    url(
        r'^investment-support-directory/',
        include(
            investment_support_directory_urls,
            namespace='investment-support-directory',
        )
    ),
    url(
        r'^trade/investment-support-directory/',
        RedirectView.as_view(url='/investment-support-directory/')
    ),
]

handler404 = 'directory_components.views.handler404'

handler500 = 'directory_components.views.handler500'
