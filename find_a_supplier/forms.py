from captcha.fields import ReCaptchaField
from directory_constants import choices
from directory_components import fields, forms, widgets
from directory_validators.common import not_contains_url_or_email
from directory_forms_api_client.forms import GovNotifyActionMixin

from django.core.validators import EMPTY_VALUES
from django.forms import HiddenInput, Textarea, TextInput, ValidationError

from core.fields import IntegerField


SELECT_LABEL = 'Please select your industry'


class CheckboxSelectMultipleIgnoreEmpty(
    widgets.CheckboxSelectInlineLabelMultiple
):

    def value_from_datadict(self, data, files, name):
        values = super().value_from_datadict(data, files, name)
        if values:
            return [value for value in values if value not in EMPTY_VALUES]


class CompanySearchForm(forms.Form):

    MESSAGE_MISSING_SECTOR_TERM = 'Please specify a search term or a sector.'

    q = fields.CharField(
        label='Search by product, service or company keyword',
        max_length=255,
        widget=TextInput(
            attrs={
                'placeholder': 'Search for UK suppliers',
                'autofocus': 'autofocus',
                'dir': 'auto',
                'data-ga-id': 'search-input'
            }
        ),
        required=False,
    )
    page = IntegerField(
        required=False,
        widget=HiddenInput,
        initial=1,
    )
    sectors = fields.MultipleChoiceField(
        label='Industry expertise',
        widget=CheckboxSelectMultipleIgnoreEmpty(
            attrs={'id': 'checkbox-industry-expertise'},
            use_nice_ids=True,
        ),
        choices=choices.INDUSTRIES,
        required=False,
    )

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('q') and not cleaned_data.get('sectors'):
            raise ValidationError(self.MESSAGE_MISSING_SECTOR_TERM)
        return cleaned_data

    def clean_page(self):
        return self.cleaned_data['page'] or self.fields['page'].initial


class ContactCompanyForm(GovNotifyActionMixin, forms.Form):

    error_css_class = 'input-field-container has-error'
    TERMS_CONDITIONS_MESSAGE = (
        'Tick the box to confirm you agree to the terms and conditions.'
    )

    full_name = fields.CharField(
        label='Your full name:',
        max_length=255,
        validators=[not_contains_url_or_email],
    )
    company_name = fields.CharField(
        label='Your company name:',
        max_length=255,
        validators=[not_contains_url_or_email],
    )
    country = fields.CharField(
        max_length=255,
        validators=[not_contains_url_or_email],
    )
    email_address = fields.EmailField(
        label='Your email address:',
    )
    sector = fields.ChoiceField(
        label='Industry:',
        choices=(
            [['', SELECT_LABEL]] + list(choices.INDUSTRIES)
        ),
    )
    subject = fields.CharField(
        label='Enter a subject line for your message:',
        help_text='Maximum 200 characters.',
        max_length=200,
        validators=[not_contains_url_or_email],
    )
    body = fields.CharField(
        label='Enter your message to the UK company:',
        help_text='Maximum 1000 characters.',
        max_length=1000,
        widget=Textarea,
        validators=[not_contains_url_or_email],
    )
    captcha = ReCaptchaField()
    terms = fields.BooleanField(
        label='I agree to the great.gov.uk terms and conditions',
        error_messages={'required': TERMS_CONDITIONS_MESSAGE},
    )


def serialize_contact_company_form(cleaned_data, company_number):
    """
    Return the shape directory-api-client expects for sending a email to a
    company

    @param {dict} cleaned_data - Fields from `ContactCompanyForm`
    @returns dict

    """

    return {
        'sender_email': cleaned_data['email_address'],
        'sender_name': cleaned_data['full_name'],
        'sender_company_name': cleaned_data['company_name'],
        'sender_country': cleaned_data['country'],
        'sector': cleaned_data['sector'],
        'subject': cleaned_data['subject'],
        'body': cleaned_data['body'],
        'recipient_company_number': company_number,
    }
