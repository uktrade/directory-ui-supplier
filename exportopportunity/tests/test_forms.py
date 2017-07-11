from exportopportunity import forms

from directory_constants.constants import choices


def test_exportopportunity_form_capcha_valid(captcha_stub):
    form = forms.OpportunityForm(
        {
            'recaptcha_response_field': captcha_stub,
            'type_of_enquiry': choices.OPEN_ENDED,
            'open_ended_description': 'foobar',
            'business_model': choices.DISTRIBUTION,
            'subsector': choices.CATERING,
            'bid_value': 'badzillions',
            'bid_timing': '2017-09-09',
            'full_name': 'Testo Useri',
            'email_address': 'test@foo.com',
            'company_name': 'Acme'
         }
    )

    assert form.is_valid()
    assert 'captcha' not in form.errors
    assert isinstance(form.cleaned_data['bid_timing'], str)


def test_exportopportunity_form_captcha_invalid():
    form = forms.OpportunityForm(
        {
            'recaptcha_response_field': 'INVALID',
            'type_of_enquiry': choices.OPEN_ENDED,
            'open_ended_description': 'foobar',
            'business_model': choices.DISTRIBUTION,
            'subsector': choices.CATERING,
            'bid_value': 'badzillions',
            'bid_timing': '2017-09-09',
            'full_name': 'Testo Useri',
            'email_address': 'test@foo.com',
            'company_name': 'Acme'
        }
    )

    assert form.is_valid() is False
    assert 'captcha' in form.errors
