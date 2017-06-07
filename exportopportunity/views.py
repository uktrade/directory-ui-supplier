from django.conf import settings
from django.http import Http404
from django.views.generic.edit import FormView

from exportopportunity import forms


class SubmitExportOpportunityView(FormView):
    form_class = forms.OpportunityForm
    template_name = 'export-opportunity.html'

    def dispatch(self, *args, **kwargs):
        if not settings.FEATURE_EXPORT_OPPORTUNITY_LEAD_GENERATION_ENABLED:
            raise Http404()
        return super().dispatch(*args, **kwargs)
