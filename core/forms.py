from django.forms import Select

from directory_components import forms, fields
from django.utils.translation import ugettext as _

from directory_constants.constants import choices


class SearchForm(forms.Form):

    term = fields.CharField(
        max_length=255,
        required=False,
    )
    sectors = fields.ChoiceField(
        required=False,
        choices=(
            (('', _('All industries')),) + choices.INDUSTRIES
        ),
        widget=Select(attrs={'class': 'bidi-rtl'})
    )


class LanguageForm(forms.Form):
    lang = fields.ChoiceField(
        choices=[]  # set by __init__
    )

    def __init__(self, language_choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lang'].choices = language_choices

    def is_language_available(self, language_code):
        language_codes = [code for code, _ in self.fields['lang'].choices]
        return language_code in language_codes
