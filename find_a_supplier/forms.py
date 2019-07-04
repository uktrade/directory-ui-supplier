from captcha.fields import ReCaptchaField
from directory_constants import choices, urls
from directory_components import fields, forms, widgets
from directory_validators.common import not_contains_url_or_email
from directory_forms_api_client.forms import GovNotifyActionMixin

from django.core.validators import EMPTY_VALUES
from django.forms import (
    HiddenInput, Select, Textarea, TextInput, ValidationError
)

from django.utils.translation import ugettext as _

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
    industries = fields.MultipleChoiceField(
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
        if not cleaned_data.get('q') and not cleaned_data.get('industries'):
            raise ValidationError(self.MESSAGE_MISSING_SECTOR_TERM)
        return cleaned_data

    def clean_page(self):
        return self.cleaned_data['page'] or self.fields['page'].initial


class ContactCompanyForm(GovNotifyActionMixin, forms.Form):
    TERMS_CONDITIONS_MESSAGE = (
        'Tick the box to confirm you agree to the terms and conditions.'
    )
    TERMS_CONDITIONS_LABEL = (
        f'<p>I agree to the <a href="{urls.TERMS_AND_CONDITIONS}" '
        'target="_blank"> great.gov.uk terms and conditions </a> and I '
        'understand that:</p>'
        '<ul class="list list-bullet">'
        '<li>the Department for International Trade (DIT) is not endorsing'
        ' the character, ability, goods or services '
        'of members of the directory</li>'
        '<li>there is no legal relationship between DIT and directory members'
        '<li>DIT is not liable for any direct or indirect loss or damage '
        'that might happen after a directory member provides a good or '
        'service</li>'
        '</ul>'
    )

    given_name = fields.CharField(
        label='Given name',
        max_length=255,
        validators=[not_contains_url_or_email],
    )
    family_name = fields.CharField(
        label='Family name',
        max_length=255,
        validators=[not_contains_url_or_email],
    )
    company_name = fields.CharField(
        label='Your organisation name',
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
        label='Your industry',
        help_text='Please select your industry',
        choices=(
            [['', SELECT_LABEL]] + list(choices.INDUSTRIES)
        ),
    )
    subject = fields.CharField(
        label='Enter a subject line for your message',
        help_text='Maximum 200 characters.',
        max_length=200,
        validators=[not_contains_url_or_email],
    )
    body = fields.CharField(
        label='Enter your message to the UK company',
        help_text=(
            'Include the goods or services you’re interested in, and your '
            'country. Maximum 1000 characters.'
        ),
        max_length=1000,
        widget=Textarea,
        validators=[not_contains_url_or_email],
    )
    captcha = ReCaptchaField()
    terms = fields.BooleanField(
        label=TERMS_CONDITIONS_LABEL,
        error_messages={'required': TERMS_CONDITIONS_MESSAGE},
    )

    @property
    def serialized_data(self):
        data = super().serialized_data
        data['sector_label'] = dict(choices.INDUSTRIES)[data['sector']]
        return data


class AnonymousSubscribeForm(forms.Form):
    PLEASE_SELECT_LABEL = _('Please select an industry')
    TERMS_CONDITIONS_MESSAGE = _(
        'Tick the box to confirm you agree to the terms and conditions.'
    )
    TERMS_CONDITIONS_LABEL = (
        f'<p>I agree to the <a href="{urls.TERMS_AND_CONDITIONS}" '
        'target="_blank"> great.gov.uk terms and conditions</a>.</p>'
    )

    full_name = fields.CharField(label=_('Your name'))
    email_address = fields.EmailField(label=_('Email address'))
    sector = fields.ChoiceField(
        label=_('Industry'),
        choices=(
            [['', PLEASE_SELECT_LABEL]] + list(choices.INDUSTRIES)
        ),
        widget=Select(attrs={'data-ga-id': 'sector-input'})
    )
    company_name = fields.CharField(label=_('Company name'))
    country = fields.CharField(label=_('Country'))
    terms = fields.BooleanField(
        label=TERMS_CONDITIONS_LABEL,
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
