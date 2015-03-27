import urllib
import base64

from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase

from apps.tokens.models import (
    OAuthAuthorizationCode,
    OAuthAccessToken,
)


class AuthorizationCodeTest(TestCase):

    fixtures = ['test_credentials']

    def setUp(self):
        self.api_client = APIClient()

    def test_no_client_id(self):
        self.assertEqual(OAuthAuthorizationCode.objects.count(), 0)

        response = self.api_client.get(
            path='/web/authorize/',
        )

        self.assertEqual(OAuthAuthorizationCode.objects.count(), 0)

        self.assertContains(response, 'invalid_client')
        self.assertContains(response, 'No client id supplied')

    def test_invalid_client_id(self):
        self.assertEqual(OAuthAuthorizationCode.objects.count(), 0)

        response = self.api_client.get(
            path='/web/authorize/?client_id=bogus',
        )

        self.assertEqual(OAuthAuthorizationCode.objects.count(), 0)

        self.assertContains(response, 'invalid_client')
        self.assertContains(response, 'The client id supplied is invalid')

    def test_missing_response_type(self):
        self.assertEqual(OAuthAuthorizationCode.objects.count(), 0)

        response = self.api_client.get(
            path='/web/authorize/?client_id=testclient',
        )

        self.assertEqual(OAuthAuthorizationCode.objects.count(), 0)

        self.assertContains(response, 'invalid_request')
        self.assertContains(response, 'Invalid or missing response type')

    def test_invalid_response_type(self):
        self.assertEqual(OAuthAuthorizationCode.objects.count(), 0)

        response = self.api_client.get(
            path='/web/authorize/?client_id=testclient&response_type=bogus',
        )

        self.assertEqual(OAuthAuthorizationCode.objects.count(), 0)

        self.assertContains(response, 'invalid_request')
        self.assertContains(response, 'Invalid or missing response type')

    def test_missing_redirect_uri(self):
        self.assertEqual(OAuthAuthorizationCode.objects.count(), 0)

        response = self.api_client.get(
            path='/web/authorize/?client_id=testclient&response_type=code',
        )

        self.assertEqual(OAuthAuthorizationCode.objects.count(), 0)

        self.assertContains(response, 'invalid_uri')
        self.assertContains(response, 'No redirect URI was supplied or stored')

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

        self.assertContains(response, 'invalid_request')
        self.assertContains(response, 'The state parameter is required')

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
                'scopes': [u'foo', u'bar', u'qux'],
            },
        )

        auth_code = OAuthAuthorizationCode.objects.last()
        self.assertEqual(auth_code.redirect_uri, 'http://www.example.com')
        self.assertEqual(auth_code.scope, 'foo,bar,qux')

        self.assertRedirects(
            response,
            'http://www.example.com?state=somestate&code={}'
            .format(auth_code.code),
            fetch_redirect_response=False,
        )

        # Now we should be able to get access token
        self.assertEqual(OAuthAccessToken.objects.count(), 0)

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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], access_token.pk)
        self.assertEqual(response.data['access_token'], access_token.access_token)
        self.assertEqual(response.data['expires_at'], access_token.expires_at.isoformat())
        self.assertEqual(response.data['token_type'], 'Bearer')
        self.assertEqual(response.data['scope'], 'foo,bar,qux')

        # Auth code should be deleted once access token is returned
        self.assertEqual(OAuthAuthorizationCode.objects.count(), 0)