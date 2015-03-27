import base64
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase

from apps.tokens.models import OAuthAccessToken


class ClientCredentialsTest(TestCase):

    fixtures = ['test_credentials']

    def setUp(self):
        self.api_client = APIClient()

    def test_invalid_credentials(self):
        self.assertEqual(OAuthAccessToken.objects.count(), 0)

        response = self.api_client.post(
            path='/api/v1/tokens/',
            data={},
            HTTP_AUTHORIZATION='Basic: {}'.format(
                base64.encodestring('bogus:bogus'))
        )

        self.assertEqual(OAuthAccessToken.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'invalid_client')
        self.assertEqual(response.data['error_description'],
                         'Client credentials were not found in the headers or body')

    def test_missing_grant_type(self):
        self.assertEqual(OAuthAccessToken.objects.count(), 0)

        response = self.api_client.post(
            path='/api/v1/tokens/',
            data={},
            HTTP_AUTHORIZATION='Basic: {}'.format(
                base64.encodestring('testclient:testpassword')),
        )

        self.assertEqual(OAuthAccessToken.objects.count(), 0)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'invalid_request')
        self.assertEqual(response.data['error_description'],
                         'The grant type was not specified in the request')

    def test_invalid_grant_type(self):
        self.assertEqual(OAuthAccessToken.objects.count(), 0)

        response = self.api_client.post(
            path='/api/v1/tokens/',
            data={'grant_type': 'bogus'},
            HTTP_AUTHORIZATION='Basic: {}'.format(
                base64.encodestring('testclient:testpassword')),
        )

        self.assertEqual(OAuthAccessToken.objects.count(), 0)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'invalid_request')
        self.assertEqual(response.data['error_description'],
                         'Invalid grant type')

    def test_success(self):
        self.assertEqual(OAuthAccessToken.objects.count(), 0)

        response = self.api_client.post(
            path='/api/v1/tokens/',
            data={'grant_type': 'client_credentials'},
            HTTP_AUTHORIZATION='Basic: {}'.format(
                base64.encodestring('testclient:testpassword')),
        )

        access_token = OAuthAccessToken.objects.last()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], access_token.pk)
        self.assertEqual(response.data['access_token'], access_token.access_token)
        self.assertEqual(response.data['expires_at'], access_token.expires_at.isoformat())
        self.assertEqual(response.data['token_type'], 'Bearer')
        self.assertIsNone(response.data['scope'], access_token.scope)

    def test_client_credentials_can_be_passed_in_post(self):
        self.assertEqual(OAuthAccessToken.objects.count(), 0)

        response = self.api_client.post(
            path='/api/v1/tokens/',
            data={
                'grant_type': 'client_credentials',
                'client_id': 'testclient',
                'client_secret': 'testpassword',
            },
        )

        access_token = OAuthAccessToken.objects.last()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], access_token.pk)
        self.assertEqual(response.data['access_token'], access_token.access_token)
        self.assertEqual(response.data['expires_at'], access_token.expires_at.isoformat())
        self.assertEqual(response.data['token_type'], 'Bearer')
        self.assertIsNone(response.data['scope'], access_token.scope)