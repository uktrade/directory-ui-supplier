from captcha.fields import ReCaptchaField
from directory_components.context_processors import (
    urls_processor, header_footer_processor
)
from directory_constants import choices
from directory_validators.common import not_contains_url_or_email
from directory_forms_api_client.forms import EmailAPIForm

from django import forms
from django.template.loader import render_to_string

from company import widgets

SELECT_LABEL = 'Please select your industry'


class CompanySearchForm(forms.Form):

    MESSAGE_MISSING_SECTOR_TERM = 'Please specify a search term or a sector.'

    term = forms.CharField(
        label='Search by product, service or company keyword',
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search for UK suppliers',
                'autofocus': 'autofocus',
                'dir': 'auto'
            }
        ),
        required=False,
    )
    page = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput,
        initial=1,
    )
    sectors = forms.MultipleChoiceField(
        required=False,
        choices=choices.INDUSTRIES,
        widget=widgets.CheckboxSelectMultipleIgnoreEmpty(
            attrs={
                'dir': 'ltr',
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('term') and not cleaned_data.get('sectors'):
            raise forms.ValidationError(self.MESSAGE_MISSING_SECTOR_TERM)
        return cleaned_data

    def clean_page(self):
        return self.cleaned_data['page'] or self.fields['page'].initial


class ContactCompanyForm(EmailAPIForm):

    error_css_class = 'input-field-container has-error'
    TERMS_CONDITIONS_MESSAGE = (
        'Tick the box to confirm you agree to the terms and conditions.'
    )

    full_name = forms.CharField(
        label='Your full name:',
        max_length=255,
        validators=[not_contains_url_or_email],
    )
    company_name = forms.CharField(
        label='Your company name:',
        max_length=255,
        validators=[not_contains_url_or_email],
    )
    country = forms.CharField(
        max_length=255,
        validators=[not_contains_url_or_email],
    )
    email_address = forms.EmailField(
        label='Your email address:',
    )
    sector = forms.ChoiceField(
        label='Industry:',
        choices=(
            [['', SELECT_LABEL]] + list(choices.INDUSTRIES)
        ),
    )
    subject = forms.CharField(
        label='Enter a subject line for your message:',
        help_text='Maximum 200 characters.',
        max_length=200,
        validators=[not_contains_url_or_email],
    )
    body = forms.CharField(
        label='Enter your message to the UK company:',
        help_text='Maximum 1000 characters.',
        max_length=1000,
        widget=forms.Textarea,
        validators=[not_contains_url_or_email],
    )
    captcha = ReCaptchaField()
    terms = forms.BooleanField(
        label='',
        error_messages={'required': TERMS_CONDITIONS_MESSAGE},
        widget=widgets.PreventRenderWidget
    )

    def save(self, recipient_name, *args, **kwargs):
        self.recipient_name = recipient_name
        return super().save(*args, **kwargs)

    def get_context_data(self):
        return {
            **self.cleaned_data,
            **urls_processor(None),
            **header_footer_processor(None),
            'recipient_name': self.recipient_name,
        }

    @property
    def html_body(self):
        return render_to_string(
            'company/email_to_supplier.html',
            self.get_context_data(),
        )

    @property
    def text_body(self):
        return render_to_string(
            'company/email_to_supplier.txt',
            self.get_context_data(),
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
