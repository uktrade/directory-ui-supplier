from directory_cms_client import cms_api_client
from directory_cms_client.helpers import handle_cms_response_allow_404
from directory_constants import cms

from django.http import Http404
from django.shortcuts import redirect
from django.utils import translation
from django.utils.cache import set_response_etag
from django.utils.functional import cached_property

from directory_components.mixins import InternationalHeaderMixin as \
    BaseInternationalHeaderMixin

from core import helpers


class IncorrectSlug(Exception):
    def __init__(self, canonical_url, *args, **kwargs):
        self.canonical_url = canonical_url
        super().__init__(*args, **kwargs)


class SetEtagMixin:
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if request.method == 'GET':
            response.add_post_render_callback(set_response_etag)
        return response


class ActiveViewNameMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_view_name'] = self.active_view_name
        return context


class GetCMSPageMixin:

    @cached_property
    def page(self):
        response = cms_api_client.lookup_by_slug(
            slug=self.kwargs['slug'],
            draft_token=self.request.GET.get('draft_token'),
            language_code=translation.get_language(),
        )
        return self.handle_cms_response(response)

    def handle_cms_response(self, response):
        return helpers.handle_cms_response(response)


class SpecificRefererRequiredMixin:

    expected_referer_url = None

    def dispatch(self, *args, **kwargs):
        referer = self.request.META.get('HTTP_REFERER', '')
        if self.expected_referer_url not in referer:
            return redirect(self.expected_referer_url)
        return super().dispatch(*args, **kwargs)


class GetCMSComponentMixin:
    @cached_property
    def cms_component(self):
        response = cms_api_client.lookup_by_slug(
            slug=self.component_slug,
            language_code=translation.get_language(),
            service_name=cms.COMPONENTS,
        )
        return handle_cms_response_allow_404(response)

    def get_context_data(self, *args, **kwargs):

        activated_language = translation.get_language()
        activated_language_is_bidi = translation.get_language_info(
            activated_language)['bidi']

        cms_component = None
        component_is_bidi = activated_language_is_bidi

        if self.cms_component:
            cms_component = self.cms_component
            component_supports_activated_language = activated_language in \
                dict(self.cms_component['meta']['languages'])
            component_is_bidi = activated_language_is_bidi and \
                component_supports_activated_language

        return super().get_context_data(
            component_is_bidi=component_is_bidi,
            cms_component=cms_component,
            *args, **kwargs)


class NotFoundOnDisabledFeature:
    def dispatch(self, *args, **kwargs):
        if not self.flag:
            raise Http404()
        return super().dispatch(*args, **kwargs)


class SubmitFormOnGetMixin:

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        data = self.request.GET or {}
        if data:
            kwargs['data'] = data
        return kwargs

    def get(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CompanyProfileMixin:
    @cached_property
    def company(self):
        return helpers.get_company_profile(self.kwargs['company_number'])

    def get_context_data(self, **kwargs):
        company = helpers.CompanyParser(self.company)
        return super().get_context_data(
            company=company.serialize_for_template(),
            **kwargs
        )


class PersistSearchQuerystringMixin:

    @property
    def search_querystring(self):
        return self.request.GET.urlencode()

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            search_querystring=self.search_querystring,
            **kwargs,
        )


class InternationalHeaderMixin(BaseInternationalHeaderMixin):
    @property
    def international_header_area(self):
        return "find_a_supplier"
