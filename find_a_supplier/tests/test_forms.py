from unittest import mock

from django.forms.fields import Field
from directory_validators.common import not_contains_url_or_email

from find_a_supplier import forms
import pytest


REQUIRED_MESSAGE = Field.default_error_messages['required']


def test_contact_company_form_required_fields():
    form = forms.ContactCompanyForm()

    assert form.fields['given_name'].required is True
    assert form.fields['family_name'].required is True
    assert form.fields['company_name'].required is True
    assert form.fields['country'].required is True
    assert form.fields['email_address'].required is True
    assert form.fields['sector'].required is True
    assert form.fields['subject'].required is True
    assert form.fields['body'].required is True


def test_contact_company__form_length_of_fields():
    form = forms.ContactCompanyForm()

    assert form.fields['given_name'].max_length == 255
    assert form.fields['family_name'].max_length == 255
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


@mock.patch(
    'directory_forms_api_client.client.forms_api_client.submit_generic'
)
def test_contact_supplier_body_text(
    mock_submit_generic, valid_contact_company_data, captcha_stub
):
    form = forms.ContactCompanyForm(data=valid_contact_company_data)

    assert form.is_valid()

    form.save(
        template_id='foo',
        email_address='reply_to@example.com',
        form_url='/trade/some/path/',
    )

    assert form.serialized_data == {
        'email_address': valid_contact_company_data['email_address'],
        'body': valid_contact_company_data['body'],
        'company_name': valid_contact_company_data['company_name'],
        'given_name': valid_contact_company_data['given_name'],
        'family_name': valid_contact_company_data['family_name'],
        'terms': True,
        'sector': valid_contact_company_data['sector'],
        'sector_label': 'Aerospace',
        'country': valid_contact_company_data['country'],
        'subject': valid_contact_company_data['subject'],
        'captcha': captcha_stub,
    }


def test_contact_company_validators():
    form = forms.ContactCompanyForm({})
    validator = not_contains_url_or_email

    assert validator in form.fields['given_name'].validators
    assert validator in form.fields['family_name'].validators
    assert validator in form.fields['company_name'].validators
    assert validator in form.fields['country'].validators
    assert validator in form.fields['subject'].validators
    assert validator in form.fields['body'].validators


def test_search_form():
    form = forms.CompanySearchForm(data={
        'q': '123',
        'industries': ['AEROSPACE']
    })

    assert form.is_valid() is True
    assert form.cleaned_data['q'] == '123'
    assert form.cleaned_data['industries'] == ['AEROSPACE']


def test_search_required_fields():
    form = forms.CompanySearchForm()

    assert form.fields['industries'].required is False
    assert form.fields['q'].required is False


def test_search_required_empty_sector_term():
    form = forms.CompanySearchForm(data={'q': '', 'industries': ''})

    assert form.is_valid() is False

    assert form.errors == {
        '__all__': [forms.CompanySearchForm.MESSAGE_MISSING_SECTOR_TERM]
    }


def test_serialize_anonymous_subscriber_forms():
    data = {
        'full_name': 'Jim Example',
        'email_address': 'jim@example.com',
        'sector': 'AEROSPACE',
        'company_name': 'Example corp',
        'country': 'UK',
    }
    expected = {
        'name': 'Jim Example',
        'email': 'jim@example.com',
        'sector': 'AEROSPACE',
        'company_name': 'Example corp',
        'country': 'UK',
    }
    actual = forms.serialize_anonymous_subscriber_forms(data)

    assert actual == expected


def test_subscribe_form_required():
    form = forms.AnonymousSubscribeForm()

    assert form.is_valid() is False
    assert form.fields['full_name'].required is True
    assert form.fields['email_address'].required is True
    assert form.fields['sector'].required is True
    assert form.fields['company_name'].required is True
    assert form.fields['country'].required is True
    assert form.fields['terms'].required is True


@pytest.fixture
def test_subscribe_form_accepts_valid_data(captcha_stub):
    form = forms.AnonymousSubscribeForm(data={
        'full_name': 'Jim Example',
        'email_address': 'jim@example.com',
        'sector': 'AEROSPACE',
        'company_name': 'Deutsche Bank',
        'country': 'DE',
        'terms': True,
        'g-recaptcha-response': captcha_stub
    })

    assert form.is_valid()
