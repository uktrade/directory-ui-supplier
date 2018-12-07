from django.core.urlresolvers import reverse
from django.utils import translation

from directory_constants.constants import urls

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


def test_footer_contact_link_processor_flag(settings):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'INTERNATIONAL_CONTACT_LINK_ON': True,
    }
    settings.HEADER_FOOTER_URLS_GREAT_HOME = None

    actual = context_processors.footer_contact_us_link(None)
    expected = urls.build_great_url('international/contact/')

    assert actual['footer_contact_us_link'] == expected


def test_footer_contact_link_processor_flag_off(settings):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'INTERNATIONAL_CONTACT_LINK_ON': False,
    }
    settings.HEADER_FOOTER_URLS_CONTACT_US = None

    actual = context_processors.footer_contact_us_link(None)

    assert actual['footer_contact_us_link'] == urls.CONTACT_US
