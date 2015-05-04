from django import forms

from apps.tokens.models import OAuthScope


class AuthorizeForm(forms.Form):

    authorize = forms.BooleanField()
    scopes = forms.ModelMultipleChoiceField(
        queryset=OAuthScope.objects.all(),
        widget=forms.CheckboxSelectMultiple)