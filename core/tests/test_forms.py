from core import forms


def test_lead_generation_form_required():
    form = forms.LeadGenerationForm()

    assert form.is_valid() is False
    assert form.fields['full_name'].required is True
    assert form.fields['email_address'].required is True
    assert form.fields['comment'].required is True
    assert form.fields['company_name'].required is True
    assert form.fields['country'].required is True
    assert form.fields['terms'].required is True
    assert form.fields['captcha'].required is True


def test_lead_generation_form_accepts_valid_data(captcha_stub):
    form = forms.LeadGenerationForm(
        data={
            'full_name': 'Jim Example',
            'email_address': 'jim@example.com',
            'comment': 'Hello',
            'company_name': 'Deutsche Bank',
            'country': 'Germany',
            'terms': True,
            'g-recaptcha-response': captcha_stub
        }
    )

    assert form.is_valid()
