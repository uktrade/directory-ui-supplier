from django.core.urlresolvers import resolve

from enrolment.forms import InternationalBuyerForm


def feature_flags(request):
    return {
        'features': {}
    }


def current_view_name(request):
    return {
        'active_view_name': resolve(request.path_info).url_name,
    }


def subscribe_form(request):
    return {
        'subscribe': {
            'form': InternationalBuyerForm(),
        },
    }
