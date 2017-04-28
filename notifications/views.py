from django.template.response import TemplateResponse
from django.views.generic.edit import FormView

from notifications import forms

from api_client import api_client


class AnonymousUnsubscribeView(FormView):
    form_class = forms.AnonymousUnsubscribeForm
    template_name = 'anonymous_unsubscribe.html'
    success_template_name = 'anonymous_unsubscribe_success.html'
    failure_template_name = 'anonymous_unsubscribe_error.html'

    def get_initial(self):
        if self.request.method == 'GET':
            return {
                'email': self.request.GET['email']
            }
        return {}

    def get(self, *args, **kwargs):
        if not self.request.GET.get('email'):
            return TemplateResponse(self.request, self.failure_template_name)
        return super().get(*args, **kwargs)

    def form_valid(self, form):
        response = api_client.notifications.anonymous_unsubscribe(
            signed_email_address=form.cleaned_data['email']
        )
        if response.ok:
            return TemplateResponse(self.request, self.success_template_name)
        return TemplateResponse(self.request, self.failure_template_name)
