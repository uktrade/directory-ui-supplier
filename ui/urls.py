from django.conf.urls import url
from django.views.decorators.cache import cache_page

from enrolment.views import (
    CachableTemplateView,
    InternationalLandingView,
    InternationalLandingSectorListView,
    InternationalLandingSectorDetailView,
)
from company.views import (
    PublicProfileListView,
    PublicProfileDetailView,
    SupplierCaseStudyDetailView
)


cache_me = cache_page(60 * 1)


urlpatterns = [
    url(
        r"^$",
        InternationalLandingView.as_view(),
        name="index"
    ),
    url(
        r"^thanks$",
        cache_me(CachableTemplateView.as_view(template_name="thanks.html")),
        name="thanks"
    ),
    url(
        r"^sorry$",
        cache_me(CachableTemplateView.as_view(template_name="sorry.html")),
        name="problem"
    ),
    url(
        r'^company/case-study/view/(?P<id>.+)$',
        SupplierCaseStudyDetailView.as_view(),
        name='company-case-study-view'
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
]
