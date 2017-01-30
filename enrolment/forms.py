from django import forms
from django.conf import settings
from django.utils import translation

from directory_validators.constants import choices


class LanguageForm(forms.Form):
    lang = forms.ChoiceField(choices=settings.LANGUAGES)


class InternationalBuyerForm(forms.Form):
    error_css_class = 'input-field-container has-error'
    PLEASE_SELECT_LABEL = 'Please select an industry'
    TERMS_CONDITIONS_MESSAGE = (
        'Tick the box to confirm you agree to the terms and conditions.'
    )

    full_name = forms.CharField(label='Your name')
    email_address = forms.EmailField(label='Email address')
    sector = forms.ChoiceField(
        label='Industry',
        choices=(
            [['', PLEASE_SELECT_LABEL]] + list(choices.COMPANY_CLASSIFICATIONS)
        )
    )
    company_name = forms.CharField(label='Company name')
    country = forms.CharField(label='Country')
    comment = forms.CharField(
        label=(
            "Tell us if you can't find what you were looking for, or if you "
            "want to give feedback"
        ),
        help_text='Maximum 1000 characters.',
        max_length=1000,
        widget=forms.Textarea,
        required=False,
    )
    terms = forms.BooleanField(
        error_messages={'required': TERMS_CONDITIONS_MESSAGE}
    )


def serialize_international_buyer_forms(cleaned_data):
    """
    Return the shape directory-api-client expects for saving international
    buyers.

    @param {dict} cleaned_data - All the fields in `InternationalBuyerForm`
    @returns dict

    """

    return {
        'name': cleaned_data['full_name'],
        'email': cleaned_data['email_address'],
        'sector': cleaned_data['sector'],
        'company_name': cleaned_data['company_name'],
        'country': cleaned_data['country'],
        'comment': cleaned_data.get('comment', ''),
    }


def get_language_form_initial_data():
    return {
        'lang': translation.get_language()
    }
