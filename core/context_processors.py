from core.forms import AnonymousSubscribeForm, LeadGenerationForm
from django.utils import translation
from django.conf import settings
from directory_components.context_processors import get_url, lazy_build_url


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


international_contact_url = lazy_build_url(
    'HEADER_FOOTER_URLS_GREAT_HOME', 'international/contact/')


def footer_contact_us_link(request):
    feedback_url = get_url('HEADER_FOOTER_URLS_CONTACT_US')

    if settings.FEATURE_FLAGS.get('INTERNATIONAL_CONTACT_LINK_ON'):
        footer_contact_us_link = international_contact_url
    else:
        footer_contact_us_link = feedback_url

    return {
        'footer_contact_us_link': footer_contact_us_link
    }
