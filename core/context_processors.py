from core.forms import AnonymousSubscribeForm, LeadGenerationForm
from django.utils import translation
from django.conf import settings
from directory_constants import urls


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


def footer_contact_us_link(request):
    if settings.FEATURE_FLAGS.get('INTERNATIONAL_CONTACT_LINK_ON'):
        footer_contact_us_link = urls.build_great_url('international/contact/')
    else:
        footer_contact_us_link = urls.CONTACT_US

    return {
        'footer_contact_us_link': footer_contact_us_link
    }
