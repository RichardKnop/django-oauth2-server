import urllib
import uuid

from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils.decorators import method_decorator
from django.utils import timezone

from apps.web.decorators import client_required
from apps.web.forms import AuthorizeForm
from apps.tokens.models import OAuthAuthorizationCode


class AuthorizeView(TemplateView):
    form_class = AuthorizeForm
    initial = {}
    template_name = 'web/authorize.html'

    @method_decorator(client_required)
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return self._render(request=request, form=form)

    @method_decorator(client_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid():
            print form.errors
            print request.POST
            return self._render(request=request, form=form)

        authorized = form.cleaned_data['authorize'] == 'yes'
        redirect_uri = request.GET['redirect_uri'] + '?'

        if not authorized:
            query_string = urllib.urlencode({
                'error': u'access_denied',
                'error_description': u'The user denied access to your application',
                'state': request.GET['state'],
            })
        else:
            auth_code = OAuthAuthorizationCode.objects.create(
                code=unicode(uuid.uuid4()),
                expires_at=timezone.now() + timezone.timedelta(seconds=3600),
                client=request.client,
                scope=form.cleaned_data['scopes'],
                redirect_uri=request.GET['redirect_uri'],
            )
            query_string = urllib.urlencode({
                'code': auth_code.code,
                'state': request.GET['state']
            })
        return HttpResponseRedirect(redirect_uri + query_string)

    def _render(self, request, form):
        return render(request, self.template_name, {
            'title': 'Authorize',
            'client': request.client,
            'form': form,
            'scopes': settings.OAUTH2_SERVER['SCOPES'],
        })