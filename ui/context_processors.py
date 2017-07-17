from django.conf import settings

from enrolment.forms import AnonymousSubscribeForm, LeadGenerationForm


def feature_flags(request):
    return {
        'features': {
            'FEATURE_MORE_INDUSTRIES_BUTTON_ENABLED': (
                settings.FEATURE_MORE_INDUSTRIES_BUTTON_ENABLED
            ),
            'FEATURE_COMPANY_SEARCH_VIEW_ENABLED': (
                settings.FEATURE_COMPANY_SEARCH_VIEW_ENABLED
            ),
            'FEATURE_SEARCH_FILTER_SECTOR_ENABLED': (
                settings.FEATURE_SEARCH_FILTER_SECTOR_ENABLED
            )
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
