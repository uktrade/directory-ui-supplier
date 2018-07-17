from industry import forms

from directory_validators.common import not_contains_url_or_email


def test_contact_company_validators():
    form = forms.ContactForm({})

    field_names = [
        'full_name',
        'organisation_name',
        'country',
        'body',
        'source_other',
    ]

    for field_name in field_names:
        assert not_contains_url_or_email in form.fields[field_name].validators
