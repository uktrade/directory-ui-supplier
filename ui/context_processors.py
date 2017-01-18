from enrolment.forms import InternationalBuyerForm


def feature_flags(request):
    return {
        'features': {}
    }


def subscribe_form(request):
    return {
        'subscribe': {
            'form': InternationalBuyerForm(),
        },
    }
