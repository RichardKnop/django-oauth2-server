from django.test import TestCase
from django.http import HttpRequest

from apps.tokens.decorators import authentication_required
from proj.exceptions import (
    AccessTokenRequiredException,
    InvalidAccessTokenException,
    InsufficientScopeException,
)


class AuthenticationRequiredTest(TestCase):

    fixtures = [
        'test_credentials',
        'test_scopes',
        'test_tokens',
    ]

    def test_access_token_required(self):
        def view(request, *args, **kwargs):
            return 'view returns something'
        decorated_view = authentication_required(scope='foo bar qux')(view)
        request = HttpRequest()
        with self.assertRaises(AccessTokenRequiredException):
            decorated_view(request)

    def test_invalid_access_token(self):
        def view(request, *args, **kwargs):
            return 'view returns something'
        decorated_view = authentication_required(scope='foo bar qux')(view)
        request = HttpRequest()
        request.META['HTTP_AUTHORIZATION'] = 'Bearer BOGUS_ACCESS_TOKEN'
        with self.assertRaises(InvalidAccessTokenException):
            decorated_view(request)

    def test_insufficient_scope(self):
        def view(request, *args, **kwargs):
            return 'view returns something'
        decorated_view = authentication_required(scope='bogus_scope')(view)
        request = HttpRequest()
        request.META['HTTP_AUTHORIZATION'] = 'Bearer 00ccd40e-72ca-4e79-a4b6-67c95e2e3f1c'
        with self.assertRaises(InsufficientScopeException):
            decorated_view(request)

    def test_success(self):
        def view(request, *args, **kwargs):
            return 'view returns something'
        decorated_view = authentication_required(scope='foo bar qux')(view)
        request = HttpRequest()
        request.META['HTTP_AUTHORIZATION'] = 'Bearer 00ccd40e-72ca-4e79-a4b6-67c95e2e3f1c'
        self.assertEqual(decorated_view(request), 'view returns something')