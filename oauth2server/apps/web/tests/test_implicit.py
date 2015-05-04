import urllib

from rest_framework.test import APIClient
from django.test import TestCase

from apps.tokens.models import (
    OAuthAuthorizationCode,
    OAuthAccessToken,
)


class ImplicitTest(TestCase):

    fixtures = [
        'test_credentials',
        'test_scopes',
    ]

    def setUp(self):
        self.api_client = APIClient()

    def test_success(self):
        self.assertEqual(OAuthAuthorizationCode.objects.count(), 0)

        query_string = urllib.urlencode({
            'client_id': 'testclient',
            'response_type': 'token',
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

        self.assertEqual(OAuthAuthorizationCode.objects.count(), 0)

        access_token = OAuthAccessToken.objects.last()
        self.assertEqual(access_token.scope, 'foo bar qux')

        self.assertRedirects(
            response,
            'http://www.example.com#access_token={}&expires_in={}'
            '&token_type=Bearer&state=somestate'.format(
                access_token.access_token, access_token.expires_in,
            ),
            fetch_redirect_response=False,
        )