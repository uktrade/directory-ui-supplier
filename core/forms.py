from django.forms import Select
from django.utils import translation
from django.utils.translation import ugettext as _

from directory_components import forms, fields
from directory_constants import choices


class SearchForm(forms.Form):

    term = fields.CharField(
        max_length=255,
        required=False,
    )
    industries = fields.ChoiceField(
        required=False,
        choices=(
            (('', _('All industries')),) + choices.INDUSTRIES
        ),
        widget=Select(attrs={'dir': 'ltr'})
    )


def get_language_form_initial_data():
    return {
        'lang': translation.get_language()
    }
