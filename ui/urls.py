from django.conf.urls import url
from django.conf import settings
from django.views.decorators.cache import cache_page

from enrolment.views import (
    CachableTemplateView,
    InternationalLandingView,
    InternationalLandingSectorListView,
    InternationalLandingSectorDetailView,
)
from supplier.views import SupplierProfileDetailView
from company.views import (
    PublicProfileListView,
    PublicProfileDetailView,
    SupplierCaseStudyDetailView
)
from admin.proxy import AdminProxyView


cache_me = cache_page(60 * 1)


urlpatterns = [
    url(
        r"^admin/",
        AdminProxyView.as_view(),
        name="admin_proxy"
    ),
    url(
        r"^api-static/admin/",
        AdminProxyView.as_view(),
        name="admin_proxy"
    ),
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
        r'^supplier-profile$',
        SupplierProfileDetailView.as_view(),
        name='supplier-detail'
    ),
    url(
        r'^company/case-study/view/(?P<id>.+)$',
        SupplierCaseStudyDetailView.as_view(),
        name='company-case-study-view'
    ),
]

if settings.FEATURE_PUBLIC_PROFILES_ENABLED:
    urlpatterns += [
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
    ]

if settings.FEATURE_SECTOR_LANDING_PAGES_ENABLED:
    urlpatterns += [
        url(
            r"^international/sectors$",
            InternationalLandingSectorListView.as_view(),
            name="international-sector-list"
        ),
        url(
            r"^international/sectors/(?P<slug>.+)$",
            InternationalLandingSectorDetailView.as_view(),
            name="international-sector-detail"
        ),
    ]
