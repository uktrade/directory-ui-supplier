from exportopportunity import forms


def test_opportunity_business_sector_required_fields():
    form = forms.OpportunityBusinessSectorForm()

    assert form.fields['business_model'].required is True
    assert form.fields['target_sectors'].required is True
    assert form.fields['business_model_other'].required is False
    assert form.fields['target_sectors_other'].required is False


def test_opportunity_business_sector_validation_messages():
    form = forms.OpportunityBusinessSectorForm(data={})

    assert form.errors['business_model'] == (
        [form.MESSAGE_SELECT_BUSINESS_MODEL]
    )
    assert form.errors['target_sectors'] == [form.MESSAGE_SELECT_SECTOR]


def test_opportunity_need_required_field():
    form = forms.OpportunityNeedForm()

    assert form.fields['products'].required is True
    assert form.fields['order_size'].required is True
    assert form.fields['order_deadline'].required is True
    assert form.fields['products_other'].required is False
    assert form.fields['additional_requirements'].required is False


def test_opportunity_need_validation_messages():
    form = forms.OpportunityNeedForm(data={})

    assert form.errors['order_deadline'] == [form.MESSAGE_SELECT_TIMESCALE]


def test_opportunity_contact_details_required_fields():
    form = forms.OpportunityContactDetailsForm()

    assert form.fields['full_name'].required is True
    assert form.fields['job_title'].required is True
    assert form.fields['email_address'].required is True
    assert form.fields['email_address_confirm'].required is True
    assert form.fields['company_name'].required is True
    assert form.fields['company_website'].required is True
    assert form.fields['phone_number'].required is True
    assert form.fields['contact_preference'].required is True
    assert form.fields['terms_agreed'].required is True
    assert form.fields['captcha'].required is True


def test_opportunity_contact_details_email_different():
    form = forms.OpportunityContactDetailsForm(data={
        'email_address': 'a@example.com',
        'email_address_confirm': 'b@example.com'
    })

    assert form.is_valid() is False
    assert form.errors['email_address'] == [form.MESSAGE_EMAIL_MISMATCH]


def test_opportunity_contact_details_email_same():
    form = forms.OpportunityContactDetailsForm(data={
        'email_address': 'a@example.com',
        'email_address_confirm': 'a@example.com'
    })

    assert form.is_valid() is False
    assert 'email_address' not in form.errors


def test_opportunity_contact_details_validation_message():
    form = forms.OpportunityContactDetailsForm(data={})

    assert form.errors['terms_agreed'] == [form.MESSAGE_TERMS_CONDITIONS]
