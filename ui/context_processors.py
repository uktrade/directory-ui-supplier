from django.conf import settings

from enrolment.forms import InternationalBuyerForm


def feature_flags(request):
    return {
        'features': {
        }
    }


def subscribe_form(request):
    return {
        'subscribe': {
            'form': InternationalBuyerForm(),
        },
    }


def analytics(request):
    return {
        'analytics': {
            'GOOGLE_TAG_MANAGER_ID': settings.GOOGLE_TAG_MANAGER_ID,
            'GOOGLE_TAG_MANAGER_ENV': settings.GOOGLE_TAG_MANAGER_ENV,
        }
    }
