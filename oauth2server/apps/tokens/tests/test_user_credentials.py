import base64

from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.conf import settings

from apps.tokens.models import (
    OAuthAccessToken,
    OAuthRefreshToken,
)


class UserCredentialsTest(TestCase):

    fixtures = [
        'test_credentials',
        'test_scopes',
    ]

    def setUp(self):
        self.api_client = APIClient()

    def test_missing_client_credentials(self):
        self.assertEqual(OAuthAccessToken.objects.count(), 0)
        self.assertEqual(OAuthRefreshToken.objects.count(), 0)

        response = self.api_client.post(
            path='/api/v1/tokens/',
            data={
                'grant_type': 'password',
                'username': 'john@doe.com',
                'password': 'testpassword',
            },
        )

        self.assertEqual(OAuthAccessToken.objects.count(), 0)
        self.assertEqual(OAuthRefreshToken.objects.count(), 0)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], u'invalid_client')
        self.assertEqual(response.data['error_description'],
                         u'Client credentials were not found in the headers or body')

    def test_invalid_client_credentials(self):
        self.assertEqual(OAuthAccessToken.objects.count(), 0)
        self.assertEqual(OAuthRefreshToken.objects.count(), 0)

        response = self.api_client.post(
            path='/api/v1/tokens/',
            data={
                'grant_type': 'password',
                'username': 'john@doe.com',
                'password': 'testpassword',
            },
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
            data={
                'grant_type': 'password',
                'username': 'john@doe.com',
                'password': 'testpassword',
            },
            HTTP_AUTHORIZATION='Basic: {}'.format(
                base64.encodestring('testclient:testpassword')),
        )

        self.assertEqual(OAuthAccessToken.objects.count(), 1)
        self.assertEqual(OAuthRefreshToken.objects.count(), 1)
        access_token = OAuthAccessToken.objects.last()
        refresh_token = OAuthRefreshToken.objects.last()

        self.assertEqual(access_token.client.client_id, 'testclient')
        self.assertEqual(access_token.user.email, 'john@doe.com')
        self.assertEqual(access_token.refresh_token, refresh_token)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], access_token.pk)
        self.assertEqual(response.data['access_token'], access_token.access_token)
        self.assertEqual(response.data['expires_in'], 3600)
        self.assertEqual(response.data['token_type'], 'Bearer')
        self.assertEqual(response.data['scope'], 'foo bar qux')
        self.assertEqual(response.data['refresh_token'], refresh_token.refresh_token)