from directory_validators.constants import choices

from django.forms.fields import Field

from company import forms, validators


REQUIRED_MESSAGE = Field.default_error_messages['required']


def test_public_profile_search_form_default_page():
    data = {
        'sectors': choices.COMPANY_CLASSIFICATIONS[1][0]
    }
    form = forms.PublicProfileSearchForm(data=data)

    assert form.is_valid() is True
    assert form.cleaned_data['page'] == 1


def test_public_profile_search_form_specified_page():
    data = {
        'sectors': choices.COMPANY_CLASSIFICATIONS[1][0],
        'page': 3
    }
    form = forms.PublicProfileSearchForm(data=data)

    assert form.is_valid() is True
    assert form.cleaned_data['page'] == 3


def test_public_profile_search_form_not_require_sectors():
    form = forms.PublicProfileSearchForm()

    assert form.fields['sectors'].required is False


def test_public_profile_search_form_valid_data():
    data = {
        'sectors': choices.COMPANY_CLASSIFICATIONS[1][0],
    }
    form = forms.PublicProfileSearchForm(data=data)

    assert form.is_valid() is True


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
    form = forms.ContactCompanyForm({'recaptcha_response_field': captcha_stub})

    form.is_valid()

    assert 'captcha' not in form.errors


def test_contact_company_form_captcha_valid():
    form = forms.ContactCompanyForm({'recaptcha_response_field': 'INVALID'})

    form.is_valid()

    assert 'captcha' in form.errors


def test_contact_company_validators():
    form = forms.ContactCompanyForm({})
    validator = validators.not_contains_url

    assert validator in form.fields['full_name'].validators
    assert validator in form.fields['company_name'].validators
    assert validator in form.fields['country'].validators
    assert validator in form.fields['subject'].validators
    assert validator in form.fields['body'].validators


def test_contact_company_terms_custom_render():
    form = forms.ContactCompanyForm()
    html = str(form)

    assert 'terms' not in html


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
        'recipient_company_number': '01234567',
    }
    actual = forms.serialize_contact_company_form(data, '01234567')

    assert actual == expected


def test_search_form():
    form = forms.CompanySearchForm(data={'term': '123'})

    assert form.fields['term'].required is True
    assert form.is_valid() is True
    assert form.cleaned_data['term'] == '123'
