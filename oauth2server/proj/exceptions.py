from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _


class ClientCredentialsRequiredException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_error = u'invalid_client'
    default_detail = _(u'Client credentials were not found in the headers or body')


class InvalidClientCredentialsException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_error = u'invalid_client'
    default_detail = _(u'Invalid client credentials')


class InvalidUserCredentialsException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_error = u'invalid_user'
    default_detail = _(u'Invalid user credentials')


class ExpiredAuthorizationCodeException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_error = u'access_denied'
    default_detail = _(u'Authorization code has expired')


class ExpiredRefreshTokenException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_error = u'expired_token'
    default_detail = _(u'Refresh token has expired')


class GrantTypeRequiredException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_error = u'invalid_request'
    default_detail = _(u'The grant type was not specified in the request')


class InvalidGrantTypeException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_error = u'invalid_request'
    default_detail = _(u'Invalid grant type')


class CodeRequiredException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_error = u'invalid_request'
    default_detail = _(u'The code parameter is required')


class UsernameRequiredException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_error = u'invalid_request'
    default_detail = _(u'The username parameter is required')


class PasswordRequiredException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_error = u'invalid_request'
    default_detail = _(u'The password parameter is required')


class RefreshTokenRequiredException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_error = u'invalid_request'
    default_detail = _(u'The refresh token parameter is required')


class AccessTokenRequiredException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_error = u'invalid_request'
    default_detail = _(u'The access token is required')


class InvalidAccessTokenException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_error = u'invalid_token'
    default_detail = u'The access token provided is invalid'


class ExpiredAccessTokenException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_error = u'expired_token'
    default_detail = u'The access token provided has expired'


class InsufficientScopeException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_error = u'insufficient_scope'
    default_detail = u'The request requires higher privileges than provided by the access token'


class AuthorizationCodeNotFoundException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_error = u'invalid_request'
    default_detail = _(u'Authorization code not found')


class RefreshTokenNotFoundException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_error = u'invalid_request'
    default_detail = _(u'Refresh token not found')


def custom_exception_handler(exc, context):
    """
    Formats REST exceptions like:
    {
        "error": "error_code",
        "error_description": "description of the error",
    }
    :param exc: Exception
    :return: Response
    """
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if not response:
        # Unhandled exceptions (500 internal server errors)
        response = Response(data={
            'error': 'server_error',
            'error_description': unicode(exc),
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response

    if hasattr(exc, 'default_error'):
        response.data['error'] = exc.default_error
    else:
        response.data['error'] = 'api_error'

    if hasattr(exc, 'default_detail'):
        response.data['error_description'] = exc.default_detail
    elif 'detail' in response.data:
        response.data['error_description'] = response.data['details']

    if 'detail' in response.data:
        del response.data['detail']

    return response