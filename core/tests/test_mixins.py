import pytest
import requests_mock

from django.views.generic import TemplateView
from django.utils import translation

from core import mixins


@pytest.mark.parametrize('method,expected', (
    ('get', '"5c4183c52a1ada6c0953ea85c8e42dad"'),
    ('post', None),
    ('patch', None),
    ('put', None),
    ('delete', None),
    ('head', None),
    ('options', None),
))
def test_set_etag_mixin(rf, method, expected):
    class MyView(mixins.SetEtagMixin, TemplateView):

        template_name = 'core/base.html'

        def post(self, *args, **kwargs):
            return super().get(*args, **kwargs)

        def patch(self, *args, **kwargs):
            return super().get(*args, **kwargs)

        def put(self, *args, **kwargs):
            return super().get(*args, **kwargs)

        def delete(self, *args, **kwargs):
            return super().get(*args, **kwargs)

        def head(self, *args, **kwargs):
            return super().get(*args, **kwargs)

        def options(self, *args, **kwargs):
            return super().get(*args, **kwargs)

    request = getattr(rf, method)('/')
    request.sso_user = None
    view = MyView.as_view()
    response = view(request)

    response.render()
    assert response.get('Etag') == expected


@pytest.mark.parametrize('view_class', mixins.SetEtagMixin.__subclasses__())
def test_cached_views_not_dynamic(rf, settings, view_class):
    # exception will be raised if the views perform http request, which are an
    # indicator that the views rely on dynamic data.
    with requests_mock.mock():
        view = view_class.as_view()
        request = rf.get('/')
        request.LANGUAGE_CODE = 'en-gb'
        # highlights if the view tries to interact with the session, which is
        # also an indicator that the view relies on dynamic data.
        request.session = None
        response = view(request)
        assert response.status_code == 200


def test_cms_language_switcher_one_language(rf):
    class MyView(mixins.CMSLanguageSwitcherMixin, TemplateView):

        template_name = 'core/base.html'

        def get_context_data(self, *args, **kwargs):
            page = {
                'meta': {'languages': [('en-gb', 'English')]}
            }
            return super().get_context_data(page=page, *args, **kwargs)

    request = rf.get('/')
    with translation.override('de'):
        response = MyView.as_view()(request)

    assert response.status_code == 200
    assert response.context_data['language_switcher']['show'] is False


def test_cms_language_switcher_active_language_unavailable(rf):

    class MyView(mixins.CMSLanguageSwitcherMixin, TemplateView):

        template_name = 'core/base.html'

        def get_context_data(self, *args, **kwargs):
            page = {
                'meta': {
                    'languages': [('en-gb', 'English'), ('de', 'German')]
                }
            }
            return super().get_context_data(page=page, *args, **kwargs)

    request = rf.get('/')
    with translation.override('fr'):
        response = MyView.as_view()(request)

    assert response.status_code == 200
    assert response.context_data['language_switcher']['show'] is False


def test_cms_language_switcher_active_language_available(rf):

    class MyView(mixins.CMSLanguageSwitcherMixin, TemplateView):

        template_name = 'core/base.html'

        def get_context_data(self, *args, **kwargs):
            page = {
                'meta': {
                    'languages': [('en-gb', 'English'), ('de', 'German')]
                }
            }
            return super().get_context_data(page=page, *args, **kwargs)

    request = rf.get('/')
    with translation.override('de'):
        response = MyView.as_view()(request)

    assert response.status_code == 200
    context = response.context_data['language_switcher']
    assert context['show'] is True
    assert context['form'].initial['lang'] == 'de'
