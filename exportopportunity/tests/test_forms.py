from exportopportunity import forms


def test_exportopportunity_form_capcha_valid(captcha_stub):
    form = forms.OpportunityForm({'recaptcha_response_field': captcha_stub})

    form.is_valid()

    assert 'captcha' not in form.errors


def test_exportopportunity_form_captcha_valid():
    form = forms.OpportunityForm({'recaptcha_response_field': 'INVALID'})

    form.is_valid()

    assert 'captcha' in form.errors
