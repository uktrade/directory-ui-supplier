from django import forms
from django.utils.translation import ugettext as _

from directory_constants.constants import choices


class SearchForm(forms.Form):

    term = forms.CharField(
        max_length=255,
        required=False,
    )
    sectors = forms.ChoiceField(
        required=False,
        choices=(
            (('', _('All industries')),) + choices.INDUSTRIES
        )
    )


class LanguageForm(forms.Form):
    lang = forms.ChoiceField(
        choices=[]  # set by __init__
    )

    def __init__(self, language_choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lang'].choices = language_choices

    def is_language_available(self, language_code):
        language_codes = [code for code, _ in self.fields['lang'].choices]
        return language_code in language_codes
