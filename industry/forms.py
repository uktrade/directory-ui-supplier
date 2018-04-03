from django.forms import Textarea
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

from directory_constants.constants import choices
from directory_components import forms, fields


class ContactForm(forms.Form):

    full_name = fields.CharField(
        label=_('Full name'),
        max_length=255,
    )
    email_address = fields.URLField(
        label=_('Email address'),
    )
    sector = fields.ChoiceField(
        label=_('Industry'),
        choices=choices.INDUSTRIES,
    )
    organisation_name = fields.CharField(
        label=_('Organisation name'),
        max_length=255,
    )
    organisation_size = fields.ChoiceField(
        label=_('Organisation size (optional)'),
        choices=(('', ''),) + choices.EMPLOYEES,
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
        choices=(('', ''),),
        required=False,
    )
    terms_agreed = fields.BooleanField(
        label=mark_safe(
            'I accept the '
            '<a href="{{ directory_components_urls.home }}/terms-and-conditions/" target="_blank">great.gov.uk terms and '
            'conditions</a>'
        )
    )
