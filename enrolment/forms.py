from django import forms
from django.utils.safestring import mark_safe

from directory_validators.constants import choices
from directory_constants.constants import urls


class InternationalBuyerForm(forms.Form):
    PLEASE_SELECT_LABEL = 'Please select a sector'
    TERMS_CONDITIONS_MESSAGE = ('Tick the box to confirm you agree to '
                                'the terms and conditions.')

    full_name = forms.CharField(label='Your name')
    email_address = forms.EmailField(label='Email address')
    sector = forms.ChoiceField(
        label='Sector',
        choices=(
            [['', PLEASE_SELECT_LABEL]] + list(choices.COMPANY_CLASSIFICATIONS)
        )
    )
    terms = forms.BooleanField(
        label=mark_safe(
            'I agree to the great.gov.uk <a target="_self" '
            'href="{url}">terms and conditions</a>.'.format(
                url=urls.TERMS_AND_CONDITIONS_URL)
        ),
        error_messages={'required': TERMS_CONDITIONS_MESSAGE}
    )

    error_css_class = 'input-field-container has-error'


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
    }
