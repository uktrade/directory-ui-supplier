from django import forms


class AnonymousUnsubscribeForm(forms.Form):
    # not using EmailField because the value is signed
    email = forms.CharField(widget=forms.HiddenInput())
