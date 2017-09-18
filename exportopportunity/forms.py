from django import forms

from captcha.fields import ReCaptchaField

from directory_constants.constants import choices

from django.utils.html import mark_safe

from company.widgets import (
    CheckboxSelectInlineLabelMultiple,
    CheckboxWithInlineLabel,
)


MESSAGE_SELECT_ALL_APPLICABLE = 'Select all that apply'


class OpportunityBusinessSectorForm(forms.Form):
    error_css_class = 'input-field-container has-error'
    MESSAGE_SELECT_BUSINESS_MODEL = 'Select a type of business'
    MESSAGE_SELECT_SECTOR = 'Select a type of business'

    business_model = forms.MultipleChoiceField(
        choices=choices.BUSINESS_MODELS + (('', 'Other'),),
        label='What type of business do you have?',
        help_text=MESSAGE_SELECT_ALL_APPLICABLE,
        error_messages={
            'required': MESSAGE_SELECT_BUSINESS_MODEL
        },
        widget=CheckboxSelectInlineLabelMultiple(),
    )
    business_model_other = forms.CharField(
        label="Your other business types (optional)",
        required=False
    )
    target_sectors = forms.MultipleChoiceField(
        label='What sector do you sell to?',
        help_text=MESSAGE_SELECT_ALL_APPLICABLE,
        choices=choices.SUBSECTOR_SELECTION + (('', 'Other'),),
        error_messages={
            'required': MESSAGE_SELECT_SECTOR
        },
        widget=CheckboxSelectInlineLabelMultiple(),
    )
    target_sectors_other = forms.CharField(
        required=False,
        label="Other sectors you sell to (optional)"
    )


class OpportunityNeedForm(forms.Form):
    error_css_class = 'input-field-container has-error'
    MESSAGE_SELECT_TIMESCALE = 'Select a timescale'
    products = forms.MultipleChoiceField(
        label='What type of products are you looking for?',
        help_text=MESSAGE_SELECT_ALL_APPLICABLE,
        choices=(
            ('DISCOUNT', 'Discount'),
            ('PREMIUM', 'Premium'),
            ('', 'Other'),
        ),
        widget=CheckboxSelectInlineLabelMultiple(),
    )
    products_other = forms.CharField(
        label='Other products you are looking for (optional)',
        required=False,
    )
    order_size = forms.ChoiceField(
        label='What is the size of your order?',
        help_text='Tell us the quantity of the product you need (optional)',
        choices=(
            ('', 'Please choose an option'),
            ('1-1000', '1-1,000 items'),
            ('1000-10000', '1,000-10,000 items'),
            ('10000-100000', '10,001-100,000 items'),
            ('100000+', '100,001+ items'),
        )
    )
    order_deadline = forms.ChoiceField(
        label='When do you need the product?',
        help_text=(
            'We’ll use this information to find companies that can meet '
            'your deadline.'
        ),
        choices=(
            ('', 'Please choose an option'),
            ('1-3 MONTHS', '1 to 3 months'),
            ('3-6 MONTHS', '3 to 6 months'),
            ('6-12 MONTHS', '6 months to a year'),
            ('NA', 'N/A'),
        ),
        error_messages={
            'required': MESSAGE_SELECT_TIMESCALE
        }
    )
    additional_requirements = forms.CharField(
        label='Do you have any other requirements? (optional)',
        help_text=(
            'Be as specific as possible, including packaging, labelling or '
            'supply chain requirements'
        ),
        required=False,
    )


class OpportunityContactDetailsForm(forms.Form):
    error_css_class = 'input-field-container has-error'
    MESSAGE_TERMS_CONDITIONS = (
        'Tick the box to confirm you agree to the terms and conditions.'
    )
    MESSAGE_EMAIL_MISMATCH = 'Emails do not match.'

    full_name = forms.CharField(
        max_length=1000, label='', help_text='Full name'
    )
    job_title = forms.CharField(
        max_length=1000, label='', help_text='Job title'
    )
    email_address = forms.EmailField(label='', help_text='Email address')
    email_address_confirm = forms.EmailField(
        label='',
        help_text='Confirm email address',
    )
    company_name = forms.CharField(
        max_length=1000, label='', help_text='Company name'
    )
    company_website = forms.URLField(label='', help_text='Company website')
    phone_number = forms.CharField(
        label='',
        help_text='Pone number, including international code',
        max_length=30
    )
    contact_preference = forms.MultipleChoiceField(
        label='How would you prefer to be contacted?',
        choices=(
            ('EMAIL', 'Email'),
            ('PHONE', 'Phone'),
        ),
        widget=CheckboxSelectInlineLabelMultiple(),
    )
    terms_agreed = forms.BooleanField(
        label_suffix='',
        label=mark_safe('<hr>'),
        error_messages={'required': MESSAGE_TERMS_CONDITIONS},
        widget=CheckboxWithInlineLabel(
            label='I agree to the great.gov.uk terms and conditions',
        ),
    )
    captcha = ReCaptchaField(
        label='',
        label_suffix='',
    )

    def clean(self):
        cleaned = super().clean()
        if ('email_address' in cleaned and 'email_address_confirm' in cleaned):
            if cleaned['email_address'] != cleaned['email_address_confirm']:
                raise forms.ValidationError({
                    'email_address': self.MESSAGE_EMAIL_MISMATCH
                })
        return cleaned
