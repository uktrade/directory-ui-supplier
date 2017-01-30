from directory_constants.constants import urls

from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django import forms


class AgreeToTermsField(forms.BooleanField):
    TERMS_LABEL = _(
        'I agree to the great.gov.uk '
        '<a target="_self" href="%(url)s">terms and conditions</a>.'
    )
    TERMS_CONDITIONS_MESSAGE = _(
        'Tick the box to confirm you agree to the terms and conditions.'
    )
    error_messages = {'required': TERMS_CONDITIONS_MESSAGE}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = mark_safe(
            self.TERMS_LABEL % {'url': urls.TERMS_AND_CONDITIONS_URL}
        )
