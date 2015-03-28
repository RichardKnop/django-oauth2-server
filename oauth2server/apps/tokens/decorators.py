import base64
from rest_framework.response import Response

from apps.credentials.models import OAuthClient
from apps.tokens.models import OAuthAccessToken
from proj.exceptions import (
    GrantTypeRequiredException,
    InvalidGrantTypeException,
    CodeRequiredException,
    UsernameRequiredException,
    PasswordRequiredException,
    AccessTokenRequiredException,
    InvalidAccessTokenException,
    ExpiredAccessTokenException,
    InsufficientScopeException,
)


def authentication_required(scope):

    def _method_wrapper(view):

        def _check_access_token_in_header(request):
            if not 'HTTP_AUTHORIZATION' in request.META:
                return False

            auth_method, auth = request.META['HTTP_AUTHORIZATION'].split(': ')
            if auth_method.lower() != 'bearer':
                return False

            return auth

        def _check_access_token_in_post(request):
            if not 'access_token' in request.POST:
                return False

            return request.POST['access_token']

        def _arguments_wrapper(request, *args, **kwargs):
            access_token = _check_access_token_in_header(request=request)
            if not access_token:
                access_token = _check_access_token_in_post(request=request)

            if not access_token:
                raise AccessTokenRequiredException()

            try:
                access_token = OAuthAccessToken.object.get(
                    access_token=access_token)
            except OAuthAccessToken.DoesNotExist:
                raise InvalidAccessTokenException()

            if access_token.is_expired():
                raise ExpiredAccessTokenException()

            if scope not in access_token.scope:
                raise InsufficientScopeException()

            request.access_token = access_token
            return view(request, *args, **kwargs)

        return _arguments_wrapper

    return _method_wrapper


def client_credentials_required(view):

    def _check_client_credentials_in_header(request):
        if not 'HTTP_AUTHORIZATION' in request.META:
            return False

        auth_method, auth = request.META['HTTP_AUTHORIZATION'].split(': ')
        if auth_method.lower() != 'basic':
            return False

        client_id, client_secret = base64.b64decode(auth).split(':')
        try:
            client = OAuthClient.objects.get(client_id=client_id)
        except OAuthClient.DoesNotExist:
            return False

        if not client.verify_password(client_secret):
            return False

        return client

    def _check_client_credentials_in_post(request):
        if 'client_id' not in request.POST:
            return False
        if 'client_secret' not in request.POST:
            return False

        client_id = request.POST.get('client_id')
        client_secret = request.POST.get('client_secret')
        client = OAuthClient.objects.get(client_id=client_id)

        if not client.verify_password(client_secret):
            return False

        return client

    def _wrapper(request, *args, **kwargs):
        client = _check_client_credentials_in_header(request=request)
        if not client:
            client = _check_client_credentials_in_post(request=request)

        if not client:
            response = Response(data={
                'error': u'invalid_client',
                'error_description': u'Client credentials were not found'
                                     u' in the headers or body',
            }, status=401)
            response['WWW-Authenticate'] = 'Basic realm="django-oauth2-server"'
            return response

        request.client = client
        return view(request, *args, **kwargs)

    return _wrapper


def grant_type_required(view):

    def _wrapper(request, *args, **kwargs):
        grant_type = request.POST.get('grant_type', None)

        if not grant_type:
            raise GrantTypeRequiredException()

        valid_grant_types = (
            'client_credentials',
            'authorization_code',
            'refresh_token',
            'password',
        )
        if grant_type not in valid_grant_types:
            raise InvalidGrantTypeException()

        if grant_type == 'authorization_code' and 'code' not in request.POST:
            raise CodeRequiredException()

        if grant_type == 'password' and 'username' not in request.POST:
            raise UsernameRequiredException()

        if grant_type == 'password' and 'password' not in request.POST:
            raise PasswordRequiredException()

        request.grant_type = grant_type
        return view(request, *args, **kwargs)

    return _wrapper