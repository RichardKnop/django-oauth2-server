import base64

from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase

from apps.tokens.models import (
    OAuthAccessToken,
    OAuthRefreshToken,
)


class RefreshTokenTest(TestCase):

    fixtures = [
        'test_credentials',
        'test_scopes',
        'test_tokens',
    ]

    def setUp(self):
        self.api_client = APIClient()

    def test_refresh_token_missing(self):
        response = self.api_client.post(
            path='/api/v1/tokens/',
            data={
                'grant_type': 'refresh_token',
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], u'invalid_request')
        self.assertEqual(response.data['error_description'],
                         u'The refresh token parameter is required')

    def test_refresh_token_not_found(self):
        response = self.api_client.post(
            path='/api/v1/tokens/',
            data={
                'grant_type': 'refresh_token',
                'refresh_token': 'bogus',
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], u'invalid_request')
        self.assertEqual(response.data['error_description'],
                         u'Refresh token not found')

    def test_missing_client_credentials(self):
        self.assertEqual(OAuthAccessToken.objects.count(), 1)
        self.assertEqual(OAuthRefreshToken.objects.count(), 1)

        response = self.api_client.post(
            path='/api/v1/tokens/',
            data={
                'grant_type': 'refresh_token',
                'refresh_token': '6fd8d272-375a-4d8a-8d0f-43367dc8b791',
            },
        )

        self.assertEqual(OAuthAccessToken.objects.count(), 1)
        self.assertEqual(OAuthRefreshToken.objects.count(), 1)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], u'invalid_client')
        self.assertEqual(response.data['error_description'],
                         u'Client credentials were not found in the headers or body')

    def test_invalid_client_credentials(self):
        response = self.api_client.post(
            path='/api/v1/tokens/',
            data={
                'grant_type': 'refresh_token',
                'refresh_token': '6fd8d272-375a-4d8a-8d0f-43367dc8b791',
            },
            HTTP_AUTHORIZATION='Basic: {}'.format(
                base64.encodestring('bogus:bogus')),
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], u'invalid_client')
        self.assertEqual(response.data['error_description'],
                         u'Invalid client credentials')

    def test_refresh_token(self):
        response = self.api_client.post(
            path='/api/v1/tokens/',
            data={
                'grant_type': 'refresh_token',
                'refresh_token': '6fd8d272-375a-4d8a-8d0f-43367dc8b791',
            },
            HTTP_AUTHORIZATION='Basic: {}'.format(
                base64.encodestring('testclient:testpassword')),
        )

        self.assertEqual(OAuthAccessToken.objects.count(), 1)
        self.assertEqual(OAuthRefreshToken.objects.count(), 1)
        access_token = OAuthAccessToken.objects.last()
        refresh_token = OAuthRefreshToken.objects.last()

        self.assertNotEqual(access_token.access_token, '00ccd40e-72ca-4e79-a4b6-67c95e2e3f1c')
        self.assertNotEqual(refresh_token.refresh_token, '6fd8d272-375a-4d8a-8d0f-43367dc8b791')

        self.assertEqual(access_token.refresh_token, refresh_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], access_token.pk)
        self.assertEqual(response.data['access_token'], access_token.access_token)
        self.assertEqual(response.data['expires_in'], 3600)
        self.assertEqual(response.data['token_type'], 'Bearer')
        self.assertEqual(response.data['scope'], 'foo bar qux')
        self.assertEqual(response.data['refresh_token'], refresh_token.refresh_token)

    def test_refresh_user_token(self):
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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user_access_token = OAuthAccessToken.objects.last()

        response = self.api_client.post(
            path='/api/v1/tokens/',
            data={
                'grant_type': 'refresh_token',
                'refresh_token': response.data['refresh_token'],
            },
            HTTP_AUTHORIZATION='Basic: {}'.format(
                base64.encodestring('testclient:testpassword')),
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        refreshed_access_token = OAuthAccessToken.objects.last()

        self.assertNotEqual(refreshed_access_token.access_token, user_access_token.access_token)
        self.assertEqual(refreshed_access_token.client.client_id, 'testclient')
        self.assertEqual(refreshed_access_token.user.email, 'john@doe.com')