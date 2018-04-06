from urllib.parse import urljoin

from django.forms import Textarea, TextInput, Select
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

from directory_constants.constants import choices
from directory_components import forms, fields
from directory_components.context_processors import get_url

from industry import constants


class ContactForm(forms.Form):
    TERMS_URL = urljoin(
        get_url("HEADER_FOOTER_URLS_GREAT_HOME"), 'terms-and-conditions/'
    )

    full_name = fields.CharField(
        label=_('Full name'),
        max_length=255,
    )
    email_address = fields.EmailField(
        label=_('Email address'),
    )
    sector = fields.ChoiceField(
        label=_('Industry'),
        choices=(('', ''),) + choices.INDUSTRIES,
    )
    organisation_name = fields.CharField(
        label=_('Organisation name'),
        max_length=255,
    )
    organisation_size = fields.ChoiceField(
        label=_('Organisation size (optional)'),
        choices=choices.EMPLOYEES,
        required=False,
    )
    country = fields.CharField(
        label=_('Country'),
        max_length=255,
    )
    body = fields.CharField(
        label=_('Describe what you need'),
        help_text=_('Maximum 1000 characters.'),
        max_length=1000,
        widget=Textarea,
    )
    source = fields.ChoiceField(
        label=_('Where did you hear about us (optional)'),
        choices=(('', ''),) + constants.MARKETING_SOURCES,
        required=False,
        initial=' ',  # prevent "other" being selected by default
        widget=Select(attrs={'class': 'js-field-other-selector'})
    )
    source_other = fields.CharField(
        label="Other source (optional)",
        required=False,
        widget=TextInput(attrs={'class': 'js-field-other'}),
    )
    terms_agreed = fields.BooleanField(
        label=mark_safe(
            'I accept the <a href="{url}" target="_blank">'
            'great.gov.uk terms and conditions</a>'.format(url=TERMS_URL)
        )
    )
