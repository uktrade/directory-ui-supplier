from directory_validators.constants import choices

from django import forms


class PublicProfileSearchForm(forms.Form):
    SELECT_LABEL = 'Please select an industry'
    sectors = forms.ChoiceField(
        label='Show UK companies in:',
        choices=[['', SELECT_LABEL]] + list(choices.COMPANY_CLASSIFICATIONS),
        required=False,
    )
    page = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput,
        initial=1,
    )

    error_css_class = 'input-field-container has-error'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        first_field_name = next(field for field in self.fields)
        self.fields[first_field_name].widget.attrs['autofocus'] = 'autofocus'

    def clean_page(self):
        return self.cleaned_data['page'] or self.fields['page'].initial
