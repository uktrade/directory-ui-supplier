from django.conf.urls import url

from enrolment.views import (
    InternationalLandingView,
    InternationalLandingSectorListView,
    InternationalLandingSectorDetailView,
)
from company.views import (
    PublicProfileListView,
    PublicProfileDetailView,
    CaseStudyDetailView
)


urlpatterns = [
    url(
        r"^$",
        InternationalLandingView.as_view(),
        name="index"
    ),
    url(
        r'^suppliers$',
        PublicProfileListView.as_view(),
        name='public-company-profiles-list',
    ),
    url(
        r'^suppliers/(?P<company_number>.+)$',
        PublicProfileDetailView.as_view(),
        name='public-company-profiles-detail',
    ),
    url(
        r'^sectors$',
        InternationalLandingSectorListView.as_view(),
        name='international-sector-list',
    ),
    url(
        r'^sectors/(?P<slug>.+)$',
        InternationalLandingSectorDetailView.as_view(),
        name='international-sector-detail',
    ),
    url(
        r'^case-study/(?P<id>.+)$',
        CaseStudyDetailView.as_view(),
        name='case-study-details'
    ),
]
