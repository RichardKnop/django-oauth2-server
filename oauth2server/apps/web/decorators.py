from django.http import HttpResponse
from django.shortcuts import render

from apps.credentials.models import OAuthClient


def validate_request(view):
    """
    Validates that request contains all required data
    :param view:
    :return: _wrapper
    """

    def _error_response(request, error, error_description):
        return HttpResponse(render(request, 'web/error.html', {
            'title': 'Error',
            'error': error,
            'error_description': error_description,
        }))

    def _wrapper(request, *args, **kwargs):
        # First we check client_id and make sure it's valid
        try:
            request.client = OAuthClient.objects.get(
                client_id=request.GET['client_id'])
        except KeyError:
            return _error_response(
                request=request, error=u'invalid_client',
                error_description=u'No client id supplied')
        except OAuthClient.DoesNotExist:
            return _error_response(
                request=request, error=u'invalid_client',
                error_description=u'The client id supplied is invalid')

        # Response type is required and can only be "code" or "token"
        request.response_type = request.GET.get('response_type', None)
        if not request.response_type or request.response_type not in ('code', 'token'):
            return _error_response(
                request=request, error=u'invalid_request',
                error_description=u'Invalid or missing response type')

        # Redirect URI is required
        request.redirect_uri = request.GET.get('redirect_uri', None)
        if not request.redirect_uri:
            return _error_response(
                request=request, error=u'invalid_uri',
                error_description=u'No redirect URI was supplied or stored')

        # The state parameter is required by default for authorize redirects.
        # This is the equivalent of a CSRF token, and provides session validation for your
        # Authorize request. See the OAuth2.0 Spec for more information on state:
        # http://tools.ietf.org/html/rfc6749#section-4.1.1
        request.state = request.GET.get('state', None)
        if not request.state:
            return _error_response(
                request=request, error=u'invalid_request',
                error_description=u'The state parameter is required')

        return view(request, *args, **kwargs)
    return _wrapper