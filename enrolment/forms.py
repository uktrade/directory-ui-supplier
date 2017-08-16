from django import forms
from django.conf import settings
from django.utils import translation
from django.utils.translation import ugettext as _

from directory_constants.constants import choices


class LanguageForm(forms.Form):
    lang = forms.ChoiceField(choices=settings.LANGUAGES)


class LanguageIndustriesForm(forms.Form):
    lang = forms.ChoiceField(choices=settings.LANGUAGES_INDUSTRIY_PAGES)


class AnonymousSubscribeForm(forms.Form):
    error_css_class = 'input-field-container has-error'
    PLEASE_SELECT_LABEL = _('Please select an industry')
    TERMS_CONDITIONS_MESSAGE = _(
        'Tick the box to confirm you agree to the terms and conditions.'
    )

    full_name = forms.CharField(label=_('Your name'))
    email_address = forms.EmailField(label=_('Email address'))
    sector = forms.ChoiceField(
        label=_('Industry'),
        choices=(
            [['', PLEASE_SELECT_LABEL]] + list(choices.INDUSTRIES)
        )
    )
    company_name = forms.CharField(label=_('Company name'))
    country = forms.CharField(label=_('Country'))
    terms = forms.BooleanField(
        error_messages={'required': TERMS_CONDITIONS_MESSAGE}
    )


class LeadGenerationForm(forms.Form):
    error_css_class = 'input-field-container has-error'
    PLEASE_SELECT_LABEL = _('Please select an industry')
    TERMS_CONDITIONS_MESSAGE = _(
        'Tick the box to confirm you agree to the terms and conditions.'
    )

    full_name = forms.CharField(label=_('Your name'))
    email_address = forms.EmailField(label=_('Email address'))
    company_name = forms.CharField(label=_('Organisation name'))
    country = forms.CharField(label=_('Country'))
    comment = forms.CharField(
        label=_('Describe what you need'),
        help_text=_('Maximum 1000 characters.'),
        max_length=1000,
        widget=forms.Textarea,
    )
    terms = forms.BooleanField(
        error_messages={'required': TERMS_CONDITIONS_MESSAGE}
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
