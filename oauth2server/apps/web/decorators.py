from django.http import HttpResponse
from django.shortcuts import render

from apps.credentials.models import OAuthClient


def validate_query_string(view):
    def wrapper(request, *args, **kwargs):
        error = None

        request.state = request.GET.get('state', None)
        if not request.state:
            error = u'invalid_request'
            error_description = u'The state parameter is required'

        request.redirect_uri = request.GET.get('redirect_uri', None)
        if not request.redirect_uri:
            error = u'invalid_uri'
            error_description = u'No redirect URI was supplied or stored'

        request.response_type = request.GET.get('response_type', None)
        if not request.response_type or request.response_type not in ('code', 'token'):
            error = u'invalid_request'
            error_description = u'Invalid or missing response type'

        try:
            request.client = OAuthClient.objects.get(client_id=request.GET['client_id'])
        except KeyError:
            error = u'invalid_client'
            error_description = u'No client id supplied'
        except OAuthClient.DoesNotExist:
            error = u'invalid_client'
            error_description = u'The client id supplied is invalid'

        if error:
            return HttpResponse(render(request, 'web/error.html', {
                'title': 'Error',
                'error': error,
                'error_description': error_description,
            }))

        return view(request, *args, **kwargs)
    return wrapper