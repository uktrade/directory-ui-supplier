from django.conf.urls import url

from enrolment.views import (
    BuyerSubscribeFormView,
    InternationalLandingView,
    InternationalLandingSectorListView,
    InternationalLandingSectorDetailView,
    PrivacyCookiesView,
    TermsView,
)
from company.views import (
    PublishedProfileListView,
    PublishedProfileDetailView,
    CaseStudyDetailView,
    ContactCompanyView
)


urlpatterns = [
    url(
        r"^$",
        InternationalLandingView.as_view(),
        name="index"
    ),
    url(
        r'^suppliers$',
        PublishedProfileListView.as_view(),
        name='public-company-profiles-list',
    ),
    url(
        r'^suppliers/(?P<company_number>.+)/contact$',
        ContactCompanyView.as_view(),
        name='contact-company',
    ),
    url(
        r'^suppliers/(?P<company_number>.+)$',
        PublishedProfileDetailView.as_view(),
        name='public-company-profiles-detail',
    ),
    url(
        r'^industries$',
        InternationalLandingSectorListView.as_view(),
        name='international-sector-list',
    ),
    url(
        r'^industries/(?P<slug>.+)$',
        InternationalLandingSectorDetailView.as_view(),
        name='international-sector-detail',
    ),
    url(
        r'^case-study/(?P<id>.+)$',
        CaseStudyDetailView.as_view(),
        name='case-study-details'
    ),
    url(
        r'^privacy-policy$',
        PrivacyCookiesView.as_view(),
        name='privacy-and-cookies'
    ),
    url(
        r'^terms-and-conditions$',
        TermsView.as_view(),
        name='terms-and-conditions'
    ),
    url(
        r'^subscribe$',
        BuyerSubscribeFormView.as_view(),
        name='subscribe'
    ),
]
