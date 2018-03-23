from django.conf import settings
from django.conf.urls import url
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from django.views.static import serve

from directory_constants.constants.lead_generation import (
    FOOD_IS_GREAT, LEGAL_IS_GREAT, FRANCE, SINGAPORE,
)

import company.views
import enrolment.views
import exportopportunity.views
import industry.views
import notifications.views
import ui.sitemaps


sitemaps = {
    'static': ui.sitemaps.StaticViewSitemap,
    'industries': ui.sitemaps.SectorLandingPageSitemap,
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
        enrolment.views.LandingPageNegotiator.as_view(),
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
    # obsolete. use `public-company-profiles-detail`
    url(
        r'^suppliers/(?P<company_number>[a-zA-Z0-9]+)/$',
        company.views.PublishedProfileDetailView.as_view(),
        name='public-company-profiles-detail-slugless',
    ),
    url(
        r'^industries/$',
        enrolment.views.SectorListViewNegotiator.as_view(),
        name='sector-list',
    ),
    url(
        r'^industries/(?P<cms_page_id>[0-9]+)/(?P<slug>[\w-]+)/$',
        industry.views.SectorDetailCMSView.as_view(),
        name='sector-detail-cms-verbose',
    ),
    url(
        r'^industry-articles/(?P<cms_page_id>[0-9]+)/(?P<slug>[\w-]+)/$',
        industry.views.SectorArticleCMSView.as_view(),
        name='sector-article',
    ),
    url(
        r'^industries/(?P<slug>.+)/summary/$',
        enrolment.views.SectorDetailView.as_view(),
        {'show_proposition': False},
        name='sector-detail-summary',
    ),
    url(
        r'^industries/(?P<slug>.+)/$',
        enrolment.views.SectorDetailView.as_view(),
        {'show_proposition': True},
        name='sector-detail-verbose',
    ),

    url(
        r'^case-study/(?P<id>.+)/(?P<slug>.+)/$',
        company.views.CaseStudyDetailView.as_view(),
        name='case-study-details'
    ),
    # obsolete. use `case-study-details`
    url(
        r'^case-study/(?P<id>.+)/$',
        company.views.CaseStudyDetailView.as_view(),
        name='case-study-details-slugless',
    ),
    url(
        r'^privacy-policy/$',
        enrolment.views.PrivacyCookiesView.as_view(),
        name='privacy-and-cookies'
    ),
    url(
        r'^terms-and-conditions/$',
        enrolment.views.TermsView.as_view(),
        name='terms-and-conditions'
    ),
    url(
        r'^subscribe/$',
        enrolment.views.AnonymousSubscribeFormView.as_view(),
        name='subscribe'
    ),
    url(
        r'^feedback/$',
        enrolment.views.LeadGenerationFormView.as_view(),
        name='lead-generation'
    ),
    url(
        r'^unsubscribe/$',
        notifications.views.AnonymousUnsubscribeView.as_view(),
        name='anonymous-unsubscribe'
    ),
    url(
        r'^export-opportunity/food-is-great/france/$',
        exportopportunity.views.FoodIsGreatOpportunityWizardView.as_view(),
        {'campaign': FOOD_IS_GREAT, 'country': FRANCE},
        name='food-is-great-lead-generation-submit-france',
    ),
    url(
        r'^export-opportunity/food-is-great/singapore/$',
        exportopportunity.views.FoodIsGreatOpportunityWizardView.as_view(),
        {'campaign': FOOD_IS_GREAT, 'country': SINGAPORE},
        name='food-is-great-lead-generation-submit-singapore',
    ),

    url(
        r'^export-opportunity/legal-is-great/france/$',
        exportopportunity.views.LegalIsGreatOpportunityWizardView.as_view(),
        {'campaign': LEGAL_IS_GREAT, 'country': FRANCE},
        name='legal-is-great-lead-generation-submit-france',
    ),
    url(
        r'^export-opportunity/legal-is-great/singapore/$',
        exportopportunity.views.LegalIsGreatOpportunityWizardView.as_view(),
        {'campaign': LEGAL_IS_GREAT, 'country': SINGAPORE},
        name='legal-is-great-lead-generation-submit-singapore',
    ),
    url(
        r'^campaign/food-is-great/france/$',
        exportopportunity.views.FoodIsGreatCampaignView.as_view(),
        {'campaign': FOOD_IS_GREAT, 'country': FRANCE},
        name='food-is-great-campaign-france',
    ),
    url(
        r'^campaign/food-is-great/singapore/$',
        exportopportunity.views.FoodIsGreatCampaignView.as_view(),
        {'campaign': FOOD_IS_GREAT, 'country': SINGAPORE},
        name='food-is-great-campaign-singapore',
    ),

    url(
        r'^campaign/legal-is-great/france/$',
        exportopportunity.views.LegalIsGreatCampaignView.as_view(),
        {'campaign': LEGAL_IS_GREAT, 'country': FRANCE},
        name='legal-is-great-campaign-france',
    ),
    url(
        r'^campaign/legal-is-great/singapore/$',
        exportopportunity.views.LegalIsGreatCampaignView.as_view(),
        {'campaign': LEGAL_IS_GREAT, 'country': SINGAPORE},
        name='legal-is-great-campaign-singapore',
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
