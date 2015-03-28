import uuid

from apps.tokens.models import (
    OAuthAccessToken,
    OAuthAuthorizationCode,
    OAuthUser,
)


def factory(grant_type, request):
    if grant_type == 'client_credentials':
        return ClientCredentials(client=request.client)

    if grant_type == 'authorization_code':
        return AuthorizationCode(
            client=request.client,
            auth_code=OAuthAuthorizationCode.objects.get(
                code=request.POST['code']))

    if grant_type == 'password':
        return UserCredentials(
            client=request.client,
            user=OAuthUser.objects.get(
                email=request.POST['username']))


class AbstractGrantType(object):

    def __init__(self, client):
        self.client = client


class ClientCredentials(AbstractGrantType):

    def grant(self):
        return OAuthAccessToken.objects.create(
            access_token=unicode(uuid.uuid4()),
            expires_at=OAuthAccessToken.new_expires_at(),
            client=self.client,
        )


class UserCredentials(AbstractGrantType):

    def __init__(self, client, user):
        super(UserCredentials, self).__init__(client=client)
        self.user = user

    def grant(self):
        return OAuthAccessToken.objects.create(
            access_token=unicode(uuid.uuid4()),
            expires_at=OAuthAccessToken.new_expires_at(),
            client=self.client,
            user=self.user,
        )


class AuthorizationCode(AbstractGrantType):

    def __init__(self, client, auth_code):
        super(AuthorizationCode, self).__init__(client=client)
        self.auth_code = auth_code

    def grant(self):
        access_token = OAuthAccessToken.objects.create(
            access_token=unicode(uuid.uuid4()),
            expires_at=OAuthAccessToken.new_expires_at(),
            client=self.client,
            scope=self.auth_code.scope,
        )
        self.auth_code.delete()
        return access_token