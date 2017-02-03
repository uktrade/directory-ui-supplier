from django.core.urlresolvers import reverse

from ui import context_processors
from enrolment.forms import InternationalBuyerForm


def test_feature_flags_installed(settings):
    processors = settings.TEMPLATES[0]['OPTIONS']['context_processors']

    assert 'ui.context_processors.feature_flags' in processors


def test_feature_returns_expected_features(rf, settings):
    request = rf.get('/')
    actual = context_processors.feature_flags(request)

    assert actual == {
        'features': {}
    }


def test_subscribe_form_installed(settings):
    processors = settings.TEMPLATES[0]['OPTIONS']['context_processors']

    assert 'ui.context_processors.subscribe_form' in processors


def test_subscribe_form_exposes_form_details(rf):
    request = rf.get(reverse('index'))

    actual = context_processors.subscribe_form(request)

    assert isinstance(actual['subscribe']['form'], InternationalBuyerForm)


def test_analytics(rf, settings):
    settings.GOOGLE_TAG_MANAGER_ID = '123'
    settings.GOOGLE_TAG_MANAGER_ENV = '&thing=1'

    actual = context_processors.analytics(None)

    assert actual == {
        'analytics': {
            'GOOGLE_TAG_MANAGER_ID': '123',
            'GOOGLE_TAG_MANAGER_ENV': '&thing=1',
        }
    }


def test_analytics_installed(settings):
    processors = settings.TEMPLATES[0]['OPTIONS']['context_processors']

    assert 'ui.context_processors.analytics' in processors
