import urllib
import base64

from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.utils import timezone

from apps.tokens.models import (
    OAuthAuthorizationCode,
    OAuthAccessToken,
    OAuthRefreshToken,
)


class AuthorizationCodeTest(TestCase):

    fixtures = [
        'test_credentials',
        'test_scopes',
    ]

    def setUp(self):
        self.api_client = APIClient()

    def test_no_client_id(self):
        self.assertEqual(OAuthAuthorizationCode.objects.count(), 0)

        response = self.api_client.get(
            path='/web/authorize/',
        )

        self.assertEqual(OAuthAuthorizationCode.objects.count(), 0)

        self.assertContains(response, u'invalid_client')
        self.assertContains(response, u'No client id supplied')

    def test_invalid_client_id(self):
        self.assertEqual(OAuthAuthorizationCode.objects.count(), 0)

        response = self.api_client.get(
            path='/web/authorize/?client_id=bogus',
        )

        self.assertEqual(OAuthAuthorizationCode.objects.count(), 0)

        self.assertContains(response, u'invalid_client')
        self.assertContains(response, u'The client id supplied is invalid')

    def test_missing_response_type(self):
        self.assertEqual(OAuthAuthorizationCode.objects.count(), 0)

        response = self.api_client.get(
            path='/web/authorize/?client_id=testclient',
        )

        self.assertEqual(OAuthAuthorizationCode.objects.count(), 0)

        self.assertContains(response, u'invalid_request')
        self.assertContains(response, u'Invalid or missing response type')

    def test_invalid_response_type(self):
        self.assertEqual(OAuthAuthorizationCode.objects.count(), 0)

        response = self.api_client.get(
            path='/web/authorize/?client_id=testclient&response_type=bogus',
        )

        self.assertEqual(OAuthAuthorizationCode.objects.count(), 0)

        self.assertContains(response, u'invalid_request')
        self.assertContains(response, u'Invalid or missing response type')

    def test_missing_redirect_uri(self):
        self.assertEqual(OAuthAuthorizationCode.objects.count(), 0)

        response = self.api_client.get(
            path='/web/authorize/?client_id=testclient&response_type=code',
        )

        self.assertEqual(OAuthAuthorizationCode.objects.count(), 0)

        self.assertContains(response, u'invalid_uri')
        self.assertContains(response, u'No redirect URI was supplied or stored')

    def test_missing_state(self):
        self.assertEqual(OAuthAuthorizationCode.objects.count(), 0)

        query_string = urllib.urlencode({
            'client_id': 'testclient',
            'response_type': 'code',
            'redirect_uri': 'http://www.example.com'
        })
        response = self.api_client.get(
            path='/web/authorize/?{}'.format(query_string),
        )

        self.assertEqual(OAuthAuthorizationCode.objects.count(), 0)

        self.assertContains(response, u'invalid_request')
        self.assertContains(response, u'The state parameter is required')

    def test_success(self):
        self.assertEqual(OAuthAuthorizationCode.objects.count(), 0)

        query_string = urllib.urlencode({
            'client_id': 'testclient',
            'response_type': 'code',
            'redirect_uri': 'http://www.example.com',
            'state': 'somestate',
        })
        response = self.api_client.post(
            path='/web/authorize/?{}'.format(query_string),
            data={
                'authorize': u'yes',
                'scopes': [u'1', u'2', u'3'],
            },
        )

        auth_code = OAuthAuthorizationCode.objects.last()
        self.assertEqual(auth_code.redirect_uri, 'http://www.example.com')
        self.assertEqual(auth_code.scope, 'foo bar qux')

        self.assertRedirects(
            response,
            'http://www.example.com?state=somestate&code={}'
            .format(auth_code.code),
            fetch_redirect_response=False,
        )

        # Now we should be able to get access token
        self.assertEqual(OAuthAccessToken.objects.count(), 0)
        self.assertEqual(OAuthRefreshToken.objects.count(), 0)

        response = self.api_client.post(
            path='/api/v1/tokens/',
            data={
                'grant_type': 'authorization_code',
                'code': auth_code.code,
            },
            HTTP_AUTHORIZATION='Basic: {}'.format(
                base64.encodestring('testclient:testpassword')),
        )

        access_token = OAuthAccessToken.objects.last()
        refresh_token = OAuthRefreshToken.objects.last()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], access_token.pk)
        self.assertEqual(response.data['access_token'], access_token.access_token)
        self.assertEqual(response.data['expires_in'], 3600)
        self.assertEqual(response.data['token_type'], 'Bearer')
        self.assertEqual(response.data['scope'], 'foo bar qux')
        self.assertEqual(response.data['refresh_token'], refresh_token.refresh_token)

        # Auth code should be deleted once access token is returned
        self.assertEqual(OAuthAuthorizationCode.objects.count(), 0)

    def test_expired_code(self):
        self.assertEqual(OAuthAuthorizationCode.objects.count(), 0)

        query_string = urllib.urlencode({
            'client_id': 'testclient',
            'response_type': 'code',
            'redirect_uri': 'http://www.example.com',
            'state': 'somestate',
        })
        response = self.api_client.post(
            path='/web/authorize/?{}'.format(query_string),
            data={
                'authorize': u'yes',
                'scopes': [u'1', u'2', u'3'],
            },
        )

        auth_code = OAuthAuthorizationCode.objects.last()
        self.assertEqual(auth_code.redirect_uri, 'http://www.example.com')
        self.assertEqual(auth_code.scope, 'foo bar qux')

        self.assertRedirects(
            response,
            'http://www.example.com?state=somestate&code={}'
            .format(auth_code.code),
            fetch_redirect_response=False,
        )

        # Now let's text expired auth code does not allow us to get access token
        auth_code.expires_at = timezone.now() - timezone.timedelta(seconds=1)
        auth_code.save()

        self.assertEqual(OAuthAccessToken.objects.count(), 0)
        self.assertEqual(OAuthRefreshToken.objects.count(), 0)

        response = self.api_client.post(
            path='/api/v1/tokens/',
            data={
                'grant_type': 'authorization_code',
                'code': auth_code.code,
            },
            HTTP_AUTHORIZATION='Basic: {}'.format(
                base64.encodestring('testclient:testpassword')),
        )

        self.assertEqual(OAuthAccessToken.objects.count(), 0)
        self.assertEqual(OAuthRefreshToken.objects.count(), 0)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], u'access_denied')
        self.assertEqual(response.data['error_description'],
                         u'Authorization code has expired')

        # Expired auth code should be deleted
        self.assertEqual(OAuthAuthorizationCode.objects.count(), 0)