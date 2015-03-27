from django import forms
from django.conf import settings


try:
    SCOPES = [(k, v) for k, v in settings.OAUTH2_SERVER['SCOPES'].iteritems()]
except KeyError:
    SCOPES = ()


class AuthorizeForm(forms.Form):
    authorize = forms.BooleanField()
    scopes = forms.MultipleChoiceField(
        choices=SCOPES, widget=forms.CheckboxSelectMultiple)