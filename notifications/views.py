from directory_api_client.client import api_client
from directory_components.mixins import CountryDisplayMixin, GA360Mixin

from django.template.response import TemplateResponse
from django.views.generic.edit import FormView

from notifications import forms


class AnonymousUnsubscribeView(CountryDisplayMixin, GA360Mixin, FormView):
    form_class = forms.AnonymousUnsubscribeForm
    template_name = 'anonymous_unsubscribe.html'
    success_template_name = 'anonymous_unsubscribe_success.html'
    failure_template_name = 'anonymous_unsubscribe_error.html'

    def __init__(self):
        super().__init__()

        self.set_ga360_payload(
            page_id='FindASupplierAnonymousUnsubscribe',
            business_unit='FindASupplier',
            site_section='Notifications',
            site_subsection='AnonymousUnsubscribe'
        )

    def get_initial(self):
        if self.request.method == 'GET' and self.request.GET.get('email'):
            return {
                'email': self.request.GET['email']
            }
        return {}

    def get(self, *args, **kwargs):
        if not self.request.GET.get('email'):
            return TemplateResponse(
                self.request,
                self.failure_template_name,
                context=self.get_context_data()
            )
        return super().get(*args, **kwargs)

    def form_valid(self, form):
        response = api_client.notifications.anonymous_unsubscribe(
            signed_email_address=form.cleaned_data['email']
        )
        if response.ok:
            return TemplateResponse(
                self.request,
                self.success_template_name,
                context=self.get_context_data()
            )
        return TemplateResponse(
            self.request,
            self.failure_template_name,
            context=self.get_context_data()
        )
