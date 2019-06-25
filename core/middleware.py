from directory_components.middleware import AbstractPrefixUrlMiddleware


class PrefixUrlMiddleware(AbstractPrefixUrlMiddleware):
    prefix = '/trade/'

    def get_redirect_url(self, request):
        if request.path.startswith('/investment-support-directory/'):
            return None
        return super().get_redirect_url(request)
