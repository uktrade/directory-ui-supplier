from directory_constants.constants import urls

from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django import forms


class AgreeToTermsMixin:
    TERMS_LABEL = _(
        'I agree to the great.gov.uk '
        '<a target="_self" href="%(url)s">terms and conditions</a>.'
    )
    TERMS_CONDITIONS_MESSAGE = _(
        'Tick the box to confirm you agree to the terms and conditions.'
    )

    def create_terms_field(self):
        return forms.BooleanField(
            error_messages={'required': self.TERMS_CONDITIONS_MESSAGE},
            label=mark_safe(
                self.TERMS_LABEL % {'url': urls.TERMS_AND_CONDITIONS_URL}
            ),
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['terms'] = self.create_terms_field()
