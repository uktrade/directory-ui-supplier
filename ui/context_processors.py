from django.conf import settings

from enrolment.forms import InternationalBuyerForm


def feature_flags(request):
    return {
        'features': {
            'FEATURE_CONTACT_COMPANY_FORM_ENABLED': (
                settings.FEATURE_CONTACT_COMPANY_FORM_ENABLED
            ),
        }
    }


def subscribe_form(request):
    return {
        'subscribe': {
            'form': InternationalBuyerForm(),
        },
    }
