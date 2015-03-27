import urllib
import uuid

from django.views.generic import View
from django.shortcuts import render
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
)
from django.conf import settings
from django.utils.decorators import method_decorator
from django.utils import timezone

from apps.web.decorators import validate_query_string
from apps.web.forms import AuthorizeForm
from apps.tokens.models import OAuthAuthorizationCode


class AuthorizeView(View):
    form_class = AuthorizeForm
    initial = {}
    template_name = 'web/authorize.html'

    @method_decorator(validate_query_string)
    def dispatch(self, *args, **kwargs):
        return super(AuthorizeView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return self._render(request=request, form=form)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return self._render(request=request, form=form)

        authorized = form.cleaned_data['authorize']
        redirect_uri = request.GET['redirect_uri'] + '?'

        if not authorized:
            query_string = urllib.urlencode({
                'error': u'access_denied',
                'error_description': u'The user denied access to your application',
                'state': request.GET['state'],
            })
        else:
            try:
                code_lifetime = settings.OAUTH2_SERVER['AUTH_CODE_LIFETIME']
            except KeyError:
                code_lifetime = 3600
            auth_code = OAuthAuthorizationCode.objects.create(
                code=unicode(uuid.uuid4()),
                expires_at=timezone.now() + timezone.timedelta(seconds=code_lifetime),
                client=request.client,
                scope=','.join(form.cleaned_data['scopes']),
                redirect_uri=request.GET['redirect_uri'],
            )
            query_string = urllib.urlencode({
                'code': auth_code.code,
                'state': request.GET['state']
            })
        return HttpResponseRedirect(redirect_uri + query_string)

    def _render(self, request, form):
        return HttpResponse(render(request, self.template_name, {
            'title': 'Authorize',
            'client': request.client,
            'form': form,
            'scopes': settings.OAUTH2_SERVER['SCOPES'],
        }))