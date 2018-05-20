from django.conf import settings

from core.forms import AnonymousSubscribeForm, LeadGenerationForm


def feature_flags(request):
    return {
        'features': {
        }
    }


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


def analytics(request):
    return {
        'analytics': {
            'GOOGLE_TAG_MANAGER_ID': settings.GOOGLE_TAG_MANAGER_ID,
            'GOOGLE_TAG_MANAGER_ENV': settings.GOOGLE_TAG_MANAGER_ENV,
            'UTM_COOKIE_DOMAIN': settings.UTM_COOKIE_DOMAIN,
        }
    }
