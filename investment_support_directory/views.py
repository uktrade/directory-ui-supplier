from directory_components.mixins import CountryDisplayMixin

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic import TemplateView

from core.mixins import NotFoundOnDisabledFeature

from investment_support_directory import helpers


class FeatureFlagMixin(NotFoundOnDisabledFeature):

    @property
    def flag(self):
        return settings.FEATURE_FLAGS['INVESTMENT_SUPPORT_DIRECTORY_ON']


class CompanySearchView(FeatureFlagMixin, CountryDisplayMixin, TemplateView):
    template_name = 'investment_support_directory/search.html'


class ProfileView(FeatureFlagMixin, CountryDisplayMixin, TemplateView):
    template_name = 'investment_support_directory/profile.html'

    def get_canonical_url(self):
        kwargs = {
            'company_number': self.company['number'],
            'slug': self.company['slug'],
        }
        return reverse('investment-support-directory-profile', kwargs=kwargs)

    def get(self, *args, **kwargs):
        if self.kwargs.get('slug') != self.company['slug']:
            return redirect(to=self.get_canonical_url())
        return super().get(*args, **kwargs)

    @cached_property
    def company(self):
        return helpers.get_company_profile(self.kwargs['company_number'])

    def get_context_data(self, **kwargs):
        company = helpers.CompanyParser(self.company)
        return super().get_context_data(
            company=company.serialize_for_template(),
            **kwargs
        )
