from captcha.fields import ReCaptchaField

from directory_constants.constants import choices, urls
from directory_components import forms, fields
from directory_validators.common import not_contains_url_or_email
from directory_forms_api_client.forms import ZendeskActionMixin

from django.forms import Textarea, TextInput, Select
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.utils.safestring import mark_safe

from industry import constants


class ContactForm(ZendeskActionMixin, forms.Form):

    def __init__(self, industry_choices, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['terms_agreed'].widget.label = mark_safe(ugettext(
            'I agree to the '
            f'<a href="{urls.TERMS_AND_CONDITIONS}" target="_blank">'
            'great.gov.uk terms and conditions</a>')
        )
        self.fields['sector'].choices = industry_choices

    full_name = fields.CharField(
        label=_('Full name'),
        max_length=255,
        validators=[not_contains_url_or_email],
        widget=TextInput(
            attrs={'dir': 'auto'}
        ),
    )
    email_address = fields.EmailField(
        label=_('Email address'),
        widget=TextInput(
            attrs={'dir': 'auto'}
        ),
    )
    phone_number = fields.CharField(
        label=_('Phone number'),
        widget=TextInput(
            attrs={'dir': 'auto'}
        ),
    )
    sector = fields.ChoiceField(
        label=_('Your industry'),
        choices=[],  # set in __init__
    )
    organisation_name = fields.CharField(
        label=_('Your organisation name'),
        max_length=255,
        validators=[not_contains_url_or_email],
        widget=TextInput(
            attrs={'dir': 'auto'}
        ),
    )
    organisation_size = fields.ChoiceField(
        label=_('Size of your organisation'),
        choices=choices.EMPLOYEES,
        required=False,
    )
    country = fields.CharField(
        label=_('Your country'),
        max_length=255,
        validators=[not_contains_url_or_email],
        widget=TextInput(
            attrs={'dir': 'auto'}
        ),
    )
    body = fields.CharField(
        label=_('Describe what products or services you need'),
        help_text=_('Maximum 1000 characters.'),
        max_length=1000,
        widget=Textarea(
            attrs={'dir': 'auto'}
        ),
        validators=[not_contains_url_or_email],
    )
    source = fields.ChoiceField(
        label=_('Where did you hear about great.gov.uk?'),
        choices=(('', ''),) + constants.MARKETING_SOURCES,
        required=False,
        initial=' ',  # prevent "other" being selected by default
        widget=Select(
            attrs={'class': 'js-field-other-selector'}
        )
    )
    source_other = fields.CharField(
        label=_("Other source (optional)"),
        required=False,
        widget=TextInput(
            attrs={
                'class': 'js-field-other',
                'dir': 'auto',
            }
        ),
        validators=[not_contains_url_or_email],
    )
    terms_agreed = fields.BooleanField()
    captcha = ReCaptchaField()

    @property
    def serialized_data(self):
        # this data will be sent to zendesk. `captcha` and `terms_agreed` are
        # not useful to the zendesk user as those fields have to be present
        # for the form to be submitted.
        data = self.cleaned_data.copy()
        del data['captcha']
        del data['terms_agreed']
        return data
