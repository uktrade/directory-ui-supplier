from django.core.urlresolvers import reverse

from ui import context_processors
from enrolment.forms import InternationalBuyerForm


def test_feature_flags_installed(settings):
    processors = settings.TEMPLATES[0]['OPTIONS']['context_processors']

    assert 'ui.context_processors.feature_flags' in processors


def test_feature_returns_expected_features(rf, settings):
    settings.FEATURE_CONTACT_COMPANY_FORM_ENABLED = 'A'

    request = rf.get('/')
    actual = context_processors.feature_flags(request)

    assert actual == {
        'features': {
            'FEATURE_CONTACT_COMPANY_FORM_ENABLED': 'A',
        }
    }


def test_subscribe_form_installed(settings):
    processors = settings.TEMPLATES[0]['OPTIONS']['context_processors']

    assert 'ui.context_processors.subscribe_form' in processors


def test_subscribe_form_exposes_form_details(rf):
    request = rf.get(reverse('index'))

    actual = context_processors.subscribe_form(request)

    assert isinstance(actual['subscribe']['form'], InternationalBuyerForm)
