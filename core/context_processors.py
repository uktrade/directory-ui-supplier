from core.forms import AnonymousSubscribeForm, LeadGenerationForm
from django.utils import translation


def subscribe_form(request):
    return {
        'subscribe': {
            'form': AnonymousSubscribeForm(),
        },
    }


def lead_generation_form(request):
    return {
        'lead_generation': {
            'form': LeadGenerationForm()
        }
    }


def html_lang_attribute(request):
    return {
        'directory_components_html_lang_attribute': translation.get_language()
    }
