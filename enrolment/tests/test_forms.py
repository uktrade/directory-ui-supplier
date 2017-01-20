from django.forms.fields import Field

from enrolment import forms


REQUIRED_MESSAGE = Field.default_error_messages['required']
TERMS_CONDITIONS_MESSAGE = \
    forms.InternationalBuyerForm.TERMS_CONDITIONS_MESSAGE


def test_international_form_missing_data():
    form = forms.InternationalBuyerForm(data={})

    assert form.is_valid() is False
    assert form.errors['full_name'] == [REQUIRED_MESSAGE]
    assert form.errors['email_address'] == [REQUIRED_MESSAGE]
    assert form.errors['sector'] == [REQUIRED_MESSAGE]
    assert form.errors['company_name'] == [REQUIRED_MESSAGE]
    assert form.errors['country'] == [REQUIRED_MESSAGE]
    assert form.errors['terms'] == [TERMS_CONDITIONS_MESSAGE]


def test_international_form_accepts_valid_data():
    form = forms.InternationalBuyerForm(data={
        'full_name': 'Jim Example',
        'email_address': 'jim@example.com',
        'sector': 'AEROSPACE',
        'company_name': 'Deutsche Bank',
        'country': 'Germany',
        'terms': True
    })
    assert form.is_valid()
