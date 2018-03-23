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
