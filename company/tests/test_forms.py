from directory_validators.constants import choices

from django.forms.fields import Field

from company import forms


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
