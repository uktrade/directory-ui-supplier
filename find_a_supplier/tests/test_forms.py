from django.forms.fields import Field
from directory_validators.common import not_contains_url_or_email

from find_a_supplier import forms


REQUIRED_MESSAGE = Field.default_error_messages['required']


def test_contact_company_form_required_fields():
    form = forms.ContactCompanyForm()

    assert form.fields['full_name'].required is True
    assert form.fields['company_name'].required is True
    assert form.fields['country'].required is True
    assert form.fields['email_address'].required is True
    assert form.fields['sector'].required is True
    assert form.fields['subject'].required is True
    assert form.fields['body'].required is True


def test_contact_company__form_length_of_fields():
    form = forms.ContactCompanyForm()

    assert form.fields['full_name'].max_length == 255
    assert form.fields['company_name'].max_length == 255
    assert form.fields['country'].max_length == 255
    assert form.fields['subject'].max_length == 200
    assert form.fields['body'].max_length == 1000


def test_contact_company_form_capcha_valid(captcha_stub):
    form = forms.ContactCompanyForm({'g-recaptcha-response': captcha_stub})

    form.is_valid()

    assert 'captcha' not in form.errors


def test_contact_company_form_captcha_invalid():
    form = forms.ContactCompanyForm({})

    assert form.is_valid() is False
    assert 'captcha' in form.errors


def test_contact_company_validators():
    form = forms.ContactCompanyForm({})
    validator = not_contains_url_or_email

    assert validator in form.fields['full_name'].validators
    assert validator in form.fields['company_name'].validators
    assert validator in form.fields['country'].validators
    assert validator in form.fields['subject'].validators
    assert validator in form.fields['body'].validators


def test_serialize_contact_company_form():
    data = {
        'email_address': 'jim@example.com',
        'full_name': 'Jimmy example',
        'company_name': 'Example corp',
        'country': 'United states of whatever',
        'sector': 'AEROSPACE',
        'subject': 'Whatever',
        'body': 'This is my united states of whatever',
    }
    expected = {
        'sender_email': 'jim@example.com',
        'sender_name': 'Jimmy example',
        'sender_company_name': 'Example corp',
        'sender_country': 'United states of whatever',
        'sector': 'AEROSPACE',
        'subject': 'Whatever',
        'body': 'This is my united states of whatever',
        'recipient_company_number': '01234567'
    }
    actual = forms.serialize_contact_company_form(data, '01234567')

    assert actual == expected


def test_search_form():
    form = forms.CompanySearchForm(data={
        'q': '123',
        'sectors': ['AEROSPACE']
    })

    assert form.is_valid() is True
    assert form.cleaned_data['q'] == '123'
    assert form.cleaned_data['sectors'] == ['AEROSPACE']


def test_search_required_fields():
    form = forms.CompanySearchForm()

    assert form.fields['sectors'].required is False
    assert form.fields['q'].required is False


def test_search_required_empty_sector_term():
    form = forms.CompanySearchForm(data={'q': '', 'sectors': ''})

    assert form.is_valid() is False

    assert form.errors == {
        '__all__': [forms.CompanySearchForm.MESSAGE_MISSING_SECTOR_TERM]
    }
