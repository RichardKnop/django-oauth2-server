import uuid

from django.utils import timezone

from apps.tokens.models import (
    OAuthAccessToken,
    OAuthAuthorizationCode,
    OAuthUser,
)
from proj.exceptions import AuthorizationCodeExpired


def factory(grant_type, client, request):
    if grant_type == 'client_credentials':
        return ClientCredentialsGrantType(client=client)

    if grant_type == 'authorization_code':
        return AuthorizationCodeGrantType(
            client=client,
            auth_code=OAuthAuthorizationCode.objects.get(
                code=request.POST['code']))

    if grant_type == 'password':
        return UserCredentialsGrantType(
            client=client,
            user=OAuthUser.objects.get(
                email=request.POST['username']))


class AbstractGrantType(object):

    def __init__(self, client):
        self.client = client


class ClientCredentialsGrantType(AbstractGrantType):

    def grant(self):
        return OAuthAccessToken.objects.create(
            access_token=unicode(uuid.uuid4()),
            expires_at=OAuthAccessToken.new_expires_at(),
            client=self.client,
        )


class UserCredentialsGrantType(AbstractGrantType):

    def __init__(self, client, user):
        super(UserCredentialsGrantType, self).__init__(client=client)
        self.user = user

    def grant(self):
        return OAuthAccessToken.objects.create(
            access_token=unicode(uuid.uuid4()),
            expires_at=OAuthAccessToken.new_expires_at(),
            client=self.client,
            user=self.user,
        )


class AuthorizationCodeGrantType(AbstractGrantType):

    def __init__(self, client, auth_code):
        super(AuthorizationCodeGrantType, self).__init__(client=client)
        self.auth_code = auth_code

    def grant(self):
        if self.auth_code.expires_at < timezone.now():
            self.auth_code.delete()
            raise AuthorizationCodeExpired()
        access_token = OAuthAccessToken.objects.create(
            access_token=unicode(uuid.uuid4()),
            expires_at=OAuthAccessToken.new_expires_at(),
            client=self.client,
            scope=self.auth_code.scope,
        )
        self.auth_code.delete()
        return access_token