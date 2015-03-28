from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.conf import settings

from apps.tokens.models import (
    OAuthAccessToken,
    OAuthRefreshToken,
)


class RefreshTokenTest(TestCase):

    fixtures = ['test_credentials']

    def setUp(self):
        self.api_client = APIClient()

    def test_refresh_token(self):
        self.assertEqual(OAuthAccessToken.objects.count(), 0)
        self.assertEqual(OAuthRefreshToken.objects.count(), 0)

        response = self.api_client.post(
            path='/api/v1/tokens/',
            data={
                'grant_type': 'client_credentials',
                'client_id': 'testclient',
                'client_secret': 'testpassword',
            },
        )

        self.assertEqual(OAuthAccessToken.objects.count(), 1)
        self.assertEqual(OAuthRefreshToken.objects.count(), 1)
        access_token = OAuthAccessToken.objects.last()
        refresh_token = OAuthRefreshToken.objects.last()

        self.assertEqual(access_token.refresh_token, refresh_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.api_client.post(
            path='/api/v1/tokens/',
            data={
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token.refresh_token,
            },
        )

        self.assertEqual(OAuthAccessToken.objects.count(), 1)
        self.assertEqual(OAuthRefreshToken.objects.count(), 1)
        new_access_token = OAuthAccessToken.objects.last()
        new_refresh_token = OAuthRefreshToken.objects.last()

        self.assertNotEqual(access_token, new_access_token)
        self.assertNotEqual(refresh_token, new_refresh_token)

        self.assertEqual(access_token.refresh_token, refresh_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], new_access_token.pk)
        self.assertEqual(response.data['access_token'], new_access_token.access_token)
        self.assertEqual(response.data['expires_at'], new_access_token.expires_at.isoformat())
        self.assertEqual(response.data['token_type'], 'Bearer')
        self.assertEqual(response.data['scope'], settings.OAUTH2_SERVER['DEFAULT_SCOPE'])
        self.assertEqual(response.data['refresh_token'], new_refresh_token.refresh_token)