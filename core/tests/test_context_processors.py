from django.core.urlresolvers import reverse
from django.utils import translation

from core import context_processors, forms


def test_subscribe_form_installed(settings):
    processors = settings.TEMPLATES[0]['OPTIONS']['context_processors']

    assert 'core.context_processors.subscribe_form' in processors


def test_subscribe_form_exposes_form_details(rf):
    request = rf.get(reverse('index'))

    actual = context_processors.subscribe_form(request)

    assert isinstance(
        actual['subscribe']['form'], forms.AnonymousSubscribeForm
    )


def test_lead_generation_form_installed(settings):
    processors = settings.TEMPLATES[0]['OPTIONS']['context_processors']

    assert 'core.context_processors.lead_generation_form' in processors


def test_lead_generation_form_exposes_form_details(rf):
    request = rf.get(reverse('index'))

    actual = context_processors.lead_generation_form(request)

    assert isinstance(
        actual['lead_generation']['form'], forms.LeadGenerationForm
    )


def test_html_lang_attribute_processor_default_lang(rf):
    request = rf.get(reverse('index'))

    actual = context_processors.html_lang_attribute(request)

    assert actual['directory_components_html_lang_attribute'] == 'en-gb'


def test_html_lang_attribute_processor_set_lang(rf):
    translation.activate('fr')
    request = rf.get(reverse('index'))

    actual = context_processors.html_lang_attribute(request)

    assert actual['directory_components_html_lang_attribute'] == 'fr'
