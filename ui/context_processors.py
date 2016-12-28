from django.conf import settings
from django.core.urlresolvers import resolve


def feature_flags(request):
    return {
        'features': {}
    }


def current_view_name(request):
    return {
        'active_view_name': resolve(request.path_info).url_name,
    }
