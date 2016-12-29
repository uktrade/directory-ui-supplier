from django.core.urlresolvers import reverse

from ui import context_processors


def test_active_view_installed(settings):
    processors = settings.TEMPLATES[0]['OPTIONS']['context_processors']

    assert 'ui.context_processors.current_view_name' in processors


def test_feature_flags_installed(settings):
    processors = settings.TEMPLATES[0]['OPTIONS']['context_processors']

    assert 'ui.context_processors.feature_flags' in processors


def test_feature_returns_expected_features(rf, settings):
    request = rf.get('/')
    actual = context_processors.feature_flags(request)

    assert actual == {
        'features': {}
    }


def test_active_view_expected_features(rf, settings):
    request = rf.get(reverse('index'))
    actual = context_processors.current_view_name(request)

    assert actual == {
        'active_view_name': 'index'
    }
