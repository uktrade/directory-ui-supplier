from django import forms

from captcha.fields import ReCaptchaField


class OpportunityForm(forms.Form):
    captcha = ReCaptchaField()
