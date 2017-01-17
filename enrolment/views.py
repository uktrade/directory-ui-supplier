from django.conf import settings
from django.shortcuts import Http404
from django.template.response import TemplateResponse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from api_client import api_client
from enrolment import constants, forms


class ShowLanguageSwitcherMixin:
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['language_switcher'] = {
            'show': settings.FEATURE_LANGUAGE_SWITCHER_ENABLED,
            'form': forms.LanguageForm(
                initial=forms.get_language_form_initial_data(),
            )
        }
        return context


class BuyerSubscribeFormView(FormView):
    success_template = 'landing-page-international-success.html'
    template_name = 'subscribe.html'
    form_class = forms.InternationalBuyerForm

    def form_valid(self, form):
        data = forms.serialize_international_buyer_forms(form.cleaned_data)
        api_client.buyer.send_form(data)
        return TemplateResponse(self.request, self.success_template)


class InternationalLandingView(ShowLanguageSwitcherMixin, TemplateView):
    template_name = 'landing-page-international.html'


class InternationalLandingSectorListView(TemplateView):
    template_name = 'landing-page-international-sector-list.html'


class PrivacyCookiesView(TemplateView):
    template_name = 'privacy-and-cookies.html'


class TermsView(TemplateView):
    template_name = 'terms-and-conditions.html'


class InternationalLandingSectorDetailView(TemplateView):
    pages = {
        'health': {
            'template': 'landing-page-international-sector-detail-health.html',
            'context': constants.HEALTH_SECTOR_CONTEXT,
        },
        'tech': {
            'template': 'landing-page-international-sector-detail-tech.html',
            'context': constants.TECH_SECTOR_CONTEXT,
        },
        'creative': {
            'template': (
                'landing-page-international-sector-detail-creative.html'
            ),
            'context': constants.CREATIVE_SECTOR_CONTEXT,
        },
        'food-and-drink': {
            'template': 'landing-page-international-sector-detail-food.html',
            'context': constants.FOOD_SECTOR_CONTEXT,
        }
    }

    def dispatch(self, request, *args, **kwargs):
        if self.kwargs['slug'] not in self.pages:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        template_name = self.pages[self.kwargs['slug']]['template']
        return [template_name]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(self.pages[self.kwargs['slug']]['context'])
        context['show_proposition'] = 'verbose' in self.request.GET
        context['slug'] = self.kwargs['slug']
        return context
