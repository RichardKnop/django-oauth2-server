import uuid

from django.conf import settings
from django.utils import timezone

from apps.tokens.models import (
    OAuthAccessToken,
    OAuthAuthorizationCode,
)


def factory(grant_type, request):
    if grant_type == 'client_credentials':
        return ClientCredentials(client=request.client)

    if grant_type == 'authorization_code':
        return AuthorizationCode(
            client=request.client,
            auth_code=OAuthAuthorizationCode.objects.get(
                code=request.POST['code']))


class AbstractGrantType(object):

    def __init__(self, client):
        self.client = client

    @property
    def token_lifetime(self):
        try:
            return settings.OAUTH2_SERVER['ACCESS_TOKEN_LIFETIME']
        except KeyError:
            return 3600

    @property
    def expires_at(self):
        return timezone.now() \
            + timezone.timedelta(seconds=self.token_lifetime)


class ClientCredentials(AbstractGrantType):

    def grant(self):
        return OAuthAccessToken.objects.create(
            access_token=unicode(uuid.uuid4()),
            expires_at=self.expires_at,
            client=self.client,
        )


class AuthorizationCode(AbstractGrantType):

    def __init__(self, client, auth_code):
        super(AuthorizationCode, self).__init__(client=client)
        self.auth_code = auth_code

    def grant(self):
        access_token = OAuthAccessToken.objects.create(
            access_token=unicode(uuid.uuid4()),
            expires_at=self.expires_at,
            client=self.client,
            scope=self.auth_code.scope,
        )
        self.auth_code.delete()
        return access_token