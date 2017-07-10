from django import forms

from captcha.fields import ReCaptchaField

from directory_constants.constants import choices


class OpportunityForm(forms.Form):
    captcha = ReCaptchaField()
    type_of_enquiry = forms.ChoiceField(
        choices=choices.TYPE_OF_ENQUIRIES,
    )
    open_ended_description = forms.CharField(
        widget=forms.Textarea,
        required=False
    )
    business_model = forms.ChoiceField(
        choices=choices.BUSINESS_MODELS
    )
    subsector = forms.ChoiceField(
        choices=choices.SUBSECTOR_SELECTION
    )
    bid_value = forms.CharField(max_length=50)
    bid_timing = forms.DateField()
    full_name = forms.CharField(max_length=255)
    email_address = forms.EmailField()
    company_name = forms.CharField(max_length=255)

    def clean_bid_timing(self):
        """Return a string for the API."""
        data = self.cleaned_data['bid_timing']
        return data.isoformat()
