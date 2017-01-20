from captcha.fields import ReCaptchaField
from directory_validators.constants import choices

from django import forms


SELECT_LABEL = 'Please select an industry'


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

    full_name = forms.CharField(
        label='Your full name:',
        max_length=255,
    )
    company_name = forms.CharField(
        label='Your company name:',
        max_length=255,
    )
    country = forms.CharField(
        max_length=255,
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
    )
    body = forms.CharField(
        label='Enter your message to the UK company:',
        help_text='Maximum 1000 characters.',
        max_length=1000,
        widget=forms.Textarea
    )
    captcha = ReCaptchaField()


def serialize_contact_company_form(cleaned_data):
    """
    Return the shape directory-api-client expects for sending a email to a
    company

    @param {dict} cleaned_data - Fields from `ContactCompanyForm`
    @returns dict

    """

    return {
        'full_name': cleaned_data['full_name'],
        'company_name': cleaned_data['company_name'],
        'country': cleaned_data['country'],
        'from': cleaned_data['email_address'],
        'sector': cleaned_data['sector'],
        'subject': cleaned_data['subject'],
        'body': cleaned_data['body'],
    }
