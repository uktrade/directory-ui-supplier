from captcha.fields import ReCaptchaField

from django.conf import settings
from django.forms import Textarea
from django.forms import Select
from django.utils import translation
from django.utils.translation import ugettext as _

from directory_components import forms, fields
from directory_constants.constants import choices
from directory_validators.common import not_contains_url_or_email
from directory_validators.company import no_html


class SearchForm(forms.Form):

    term = fields.CharField(
        max_length=255,
        required=False,
    )
    sectors = fields.ChoiceField(
        required=False,
        choices=(
            (('', _('All industries')),) + choices.INDUSTRIES
        ),
        widget=Select(attrs={'class': 'bidi-rtl'})
    )


class LanguageForm(forms.Form):
    lang = fields.ChoiceField(
        choices=[]  # set by __init__
    )

    def __init__(self, language_choices=settings.LANGUAGES, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lang'].choices = language_choices

    def is_language_available(self, language_code):
        language_codes = [code for code, _ in self.fields['lang'].choices]
        return language_code in language_codes


class AnonymousSubscribeForm(forms.Form):
    error_css_class = 'input-field-container has-error'
    PLEASE_SELECT_LABEL = _('Please select an industry')
    TERMS_CONDITIONS_MESSAGE = _(
        'Tick the box to confirm you agree to the terms and conditions.'
    )

    full_name = fields.CharField(label=_('Your name'))
    email_address = fields.EmailField(label=_('Email address'))
    sector = fields.ChoiceField(
        label=_('Industry'),
        choices=(
            [['', PLEASE_SELECT_LABEL]] + list(choices.INDUSTRIES)
        )
    )
    company_name = fields.CharField(label=_('Company name'))
    country = fields.CharField(label=_('Country'))
    terms = fields.BooleanField(
        error_messages={'required': TERMS_CONDITIONS_MESSAGE}
    )


class LeadGenerationForm(forms.Form):
    error_css_class = 'input-field-container has-error'
    PLEASE_SELECT_LABEL = _('Please select an industry')
    TERMS_CONDITIONS_MESSAGE = _(
        'Tick the box to confirm you agree to the terms and conditions.'
    )

    full_name = fields.CharField(label=_('Your name'))
    email_address = fields.EmailField(label=_('Email address'))
    company_name = fields.CharField(label=_('Organisation name'))
    country = fields.CharField(label=_('Country'))
    comment = fields.CharField(
        label=_('Describe what you need'),
        help_text=_('Maximum 1000 characters.'),
        max_length=1000,
        widget=Textarea,
        validators=[no_html, not_contains_url_or_email]
    )
    terms = fields.BooleanField(
        error_messages={'required': TERMS_CONDITIONS_MESSAGE}
    )
    captcha = ReCaptchaField(
        label='',
        label_suffix='',
    )


def serialize_anonymous_subscriber_forms(cleaned_data):
    """
    Return the shape directory-api-client expects for saving international
    buyers.

    @param {dict} cleaned_data - All the fields in `AnonymousSubscribeForm`
    @returns dict

    """

    return {
        'name': cleaned_data['full_name'],
        'email': cleaned_data['email_address'],
        'sector': cleaned_data['sector'],
        'company_name': cleaned_data['company_name'],
        'country': cleaned_data['country'],
    }


def get_language_form_initial_data():
    return {
        'lang': translation.get_language()
    }
