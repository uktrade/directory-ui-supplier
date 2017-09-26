from django import forms

from captcha.fields import ReCaptchaField

from directory_constants.constants import choices

from django.conf import settings
from django.utils.html import mark_safe

from company.widgets import (
    CheckboxSelectInlineLabelMultiple,
    CheckboxWithInlineLabel,
)


MESSAGE_SELECT_ALL_APPLICABLE = 'Select all that apply'
MESSAGE_CHOOSE = 'Please choose an option'

locality_options = [[i, i.title()] for i in choices.LEAD_GENERATION_COUNTRIES]


class OpportunityBusinessSectorForm(forms.Form):
    error_css_class = 'input-field-container has-error'
    MESSAGE_SELECT_BUSINESS_MODEL = 'Select a type of business'
    MESSAGE_SELECT_SECTOR = 'Select a type of business'
    MESSAGE_UNSUPPORTED_LOCALITY = 'Sorry. We do not support that region yet.'
    OTHER = 'OTHER'

    locality = forms.ChoiceField(
        label="Which country are you based in?",
        choices=[['', MESSAGE_CHOOSE]] + locality_options + [[OTHER, 'Other']]
    )
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

    def clean_locality(self):
        if self.cleaned_data['locality'] == self.OTHER:
            raise forms.ValidationError(self.MESSAGE_UNSUPPORTED_LOCALITY)
        return self.cleaned_data['locality']


class OpportunityNeedForm(forms.Form):
    error_css_class = 'input-field-container has-error'
    MESSAGE_SELECT_TIMESCALE = 'Select a timescale'
    products = forms.MultipleChoiceField(
        label='What type of products are you looking for?',
        help_text=MESSAGE_SELECT_ALL_APPLICABLE,
        choices=choices.PRODUCT_TYPE_OPTIONS + (('', 'Other'),),
        widget=CheckboxSelectInlineLabelMultiple(),
    )
    products_other = forms.CharField(
        label='Other products you are looking for (optional)',
        required=False,
    )
    order_size = forms.ChoiceField(
        label='What is the size of your order?',
        help_text='Tell us the quantity of the product you need (optional)',
        choices=(('', MESSAGE_CHOOSE),) + choices.ORDER_SIZE_OPTIONS
    )
    order_deadline = forms.ChoiceField(
        label='When do you need the product?',
        help_text=(
            'We’ll use this information to find companies that can meet '
            'your deadline.'
        ),
        choices=(
            (('', MESSAGE_CHOOSE),) + choices.ORDER_DEADLINE_OPTIONS
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
        max_length=1000,
        widget=forms.Textarea,
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
        help_text='Phone number, including international code',
        max_length=30
    )
    contact_preference = forms.MultipleChoiceField(
        label='How would you prefer to be contacted?',
        choices=choices.CONTACT_OPTIONS,
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


class LanguageCampaignForm(forms.Form):
    def __init__(self, language_codes, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lang'].choices = [
            (key, name) for key, name in settings.LANGUAGES
            if key in language_codes
        ]

    lang = forms.ChoiceField(choices=[])  # choices set on __init__


class LanguageLeadGeneartionForm(forms.Form):
    lang = forms.ChoiceField(choices=settings.LANGUAGES_LEAD_GENERATION_PAGES)
