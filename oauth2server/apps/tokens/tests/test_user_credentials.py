import base64
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase

from apps.tokens.models import OAuthAccessToken


class UserCredentialsTest(TestCase):

    fixtures = ['test_credentials']

    def setUp(self):
        self.api_client = APIClient()

    def test_success(self):
        self.assertEqual(OAuthAccessToken.objects.count(), 0)

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

        access_token = OAuthAccessToken.objects.last()
        self.assertEqual(access_token.client.client_id, 'testclient')
        self.assertEqual(access_token.user.email, 'john@doe.com')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], access_token.pk)
        self.assertEqual(response.data['access_token'], access_token.access_token)
        self.assertEqual(response.data['expires_at'], access_token.expires_at.isoformat())
        self.assertEqual(response.data['token_type'], 'Bearer')
        self.assertIsNone(response.data['scope'], access_token.scope)