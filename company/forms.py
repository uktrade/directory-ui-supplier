from captcha.fields import ReCaptchaField
from directory_validators.constants import choices

from django import forms

from company import validators, widgets


SELECT_LABEL = 'Please select your industry'


class CompanySearchForm(forms.Form):
    term = forms.CharField(
        label='Search by product, service or company keyword',
        max_length=255,
        widget=forms.TextInput(
            attrs={'placeholder': 'Search for UK suppliers'}
        ),
        required=False,
    )
    page = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput,
        initial=1,
    )
    sector = forms.ChoiceField(
        required=False,
        widget=forms.HiddenInput,
        choices=choices.COMPANY_CLASSIFICATIONS,
    )

    def clean_page(self):
        return self.cleaned_data['page'] or self.fields['page'].initial


class PublicProfileSearchForm(forms.Form):
    sectors = forms.ChoiceField(
        label='Show UK companies in:',
        choices=[['', SELECT_LABEL]] + list(choices.COMPANY_CLASSIFICATIONS),
        required=False,
    )
    page = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput,
        initial=1,
    )

    error_css_class = 'input-field-container has-error'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        first_field_name = next(field for field in self.fields)
        self.fields[first_field_name].widget.attrs['autofocus'] = 'autofocus'

    def clean_page(self):
        return self.cleaned_data['page'] or self.fields['page'].initial


class ContactCompanyForm(forms.Form):
    error_css_class = 'input-field-container has-error'
    TERMS_CONDITIONS_MESSAGE = (
        'Tick the box to confirm you agree to the terms and conditions.'
    )

    full_name = forms.CharField(
        label='Your full name:',
        max_length=255,
        validators=[validators.not_contains_url],
    )
    company_name = forms.CharField(
        label='Your company name:',
        max_length=255,
        validators=[validators.not_contains_url],
    )
    country = forms.CharField(
        max_length=255,
        validators=[validators.not_contains_url],
    )
    email_address = forms.EmailField(
        label='Your email address:',
    )
    sector = forms.ChoiceField(
        label='Industry:',
        choices=(
            [['', SELECT_LABEL]] + list(choices.COMPANY_CLASSIFICATIONS)
        ),
    )
    subject = forms.CharField(
        label='Enter a subject line for your message:',
        help_text='Maximum 200 characters.',
        max_length=200,
        validators=[validators.not_contains_url],
    )
    body = forms.CharField(
        label='Enter your message to the UK company:',
        help_text='Maximum 1000 characters.',
        max_length=1000,
        widget=forms.Textarea,
        validators=[validators.not_contains_url],
    )
    captcha = ReCaptchaField()
    terms = forms.BooleanField(
        error_messages={'required': TERMS_CONDITIONS_MESSAGE}
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['terms'].widget = widgets.PreventRenderWidget


def serialize_contact_company_form(cleaned_data, company_number):
    """
    Return the shape directory-api-client expects for sending a email to a
    company

    @param {dict} cleaned_data - Fields from `ContactCompanyForm`
    @param {str}  company_number - the recipient's company house number
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
