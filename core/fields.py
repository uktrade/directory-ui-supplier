from directory_components.fields import DirectoryComponentsFieldMixin
from captcha.fields import ReCaptchaField

from django import forms


class IntegerField(DirectoryComponentsFieldMixin, forms.IntegerField):
    pass


class DirectoryComponentsRecaptchaField(DirectoryComponentsFieldMixin,
                                        ReCaptchaField):
    pass
