import base64

from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase

from apps.tokens.models import (
    OAuthAccessToken,
    OAuthRefreshToken,
)


class ClientCredentialsTest(TestCase):

    fixtures = [
        'test_credentials',
        'test_scopes',
    ]

    def setUp(self):
        self.api_client = APIClient()

    def test_missing_grant_type(self):
        self.assertEqual(OAuthAccessToken.objects.count(), 0)
        self.assertEqual(OAuthRefreshToken.objects.count(), 0)

        response = self.api_client.post(
            path='/api/v1/tokens/',
            data={},
        )

        self.assertEqual(OAuthAccessToken.objects.count(), 0)
        self.assertEqual(OAuthRefreshToken.objects.count(), 0)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], u'invalid_request')
        self.assertEqual(response.data['error_description'],
                         u'The grant type was not specified in the request')

    def test_invalid_grant_type(self):
        self.assertEqual(OAuthAccessToken.objects.count(), 0)
        self.assertEqual(OAuthRefreshToken.objects.count(), 0)

        response = self.api_client.post(
            path='/api/v1/tokens/',
            data={'grant_type': 'bogus'},
        )

        self.assertEqual(OAuthAccessToken.objects.count(), 0)
        self.assertEqual(OAuthRefreshToken.objects.count(), 0)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], u'invalid_request')
        self.assertEqual(response.data['error_description'],
                         u'Invalid grant type')

    def test_missing_credentials(self):
        self.assertEqual(OAuthAccessToken.objects.count(), 0)
        self.assertEqual(OAuthRefreshToken.objects.count(), 0)

        response = self.api_client.post(
            path='/api/v1/tokens/',
            data={'grant_type': 'client_credentials'},
        )

        self.assertEqual(OAuthAccessToken.objects.count(), 0)
        self.assertEqual(OAuthRefreshToken.objects.count(), 0)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], u'invalid_client')
        self.assertEqual(response.data['error_description'],
                         u'Client credentials were not found in the headers or body')

    def test_invalid_credentials(self):
        self.assertEqual(OAuthAccessToken.objects.count(), 0)
        self.assertEqual(OAuthRefreshToken.objects.count(), 0)

        response = self.api_client.post(
            path='/api/v1/tokens/',
            data={'grant_type': 'client_credentials'},
            HTTP_AUTHORIZATION='Basic: {}'.format(
                base64.encodestring('bogus:bogus')),
        )

        self.assertEqual(OAuthAccessToken.objects.count(), 0)
        self.assertEqual(OAuthRefreshToken.objects.count(), 0)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], u'invalid_client')
        self.assertEqual(response.data['error_description'],
                         u'Invalid client credentials')

    def test_success(self):
        self.assertEqual(OAuthAccessToken.objects.count(), 0)
        self.assertEqual(OAuthRefreshToken.objects.count(), 0)

        response = self.api_client.post(
            path='/api/v1/tokens/',
            data={'grant_type': 'client_credentials'},
            HTTP_AUTHORIZATION='Basic: {}'.format(
                base64.encodestring('testclient:testpassword')),
        )

        access_token = OAuthAccessToken.objects.last()
        refresh_token = OAuthRefreshToken.objects.last()

        self.assertEqual(access_token.client.client_id, 'testclient')
        self.assertIsNone(access_token.user)
        self.assertEqual(access_token.refresh_token, refresh_token)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], access_token.pk)
        self.assertEqual(response.data['access_token'], access_token.access_token)
        self.assertEqual(response.data['expires_in'], 3600)
        self.assertEqual(response.data['token_type'], 'Bearer')
        self.assertEqual(response.data['scope'], 'foo bar qux')
        self.assertEqual(response.data['refresh_token'], refresh_token.refresh_token)

    def test_client_credentials_can_be_passed_in_post(self):
        self.assertEqual(OAuthAccessToken.objects.count(), 0)
        self.assertEqual(OAuthRefreshToken.objects.count(), 0)

        response = self.api_client.post(
            path='/api/v1/tokens/',
            data={
                'grant_type': 'client_credentials',
                'client_id': 'testclient',
                'client_secret': 'testpassword',
                'scope': 'foo qux',
            },
        )

        access_token = OAuthAccessToken.objects.last()
        refresh_token = OAuthRefreshToken.objects.last()

        self.assertEqual(access_token.client.client_id, 'testclient')
        self.assertIsNone(access_token.user)
        self.assertEqual(access_token.refresh_token, refresh_token)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], access_token.pk)
        self.assertEqual(response.data['access_token'], access_token.access_token)
        self.assertEqual(response.data['expires_in'], 3600)
        self.assertEqual(response.data['token_type'], 'Bearer')
        self.assertEqual(response.data['scope'], 'foo qux')
        self.assertEqual(response.data['refresh_token'], refresh_token.refresh_token)