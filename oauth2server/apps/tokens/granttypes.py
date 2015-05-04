import uuid

from django.conf import settings

from apps.tokens.models import (
    OAuthAccessToken,
    OAuthRefreshToken,
)
from proj.exceptions import (
    ExpiredAuthorizationCodeException,
    ExpiredRefreshTokenException,
)


def factory(request):
    if request.grant_type == 'client_credentials':
        return ClientCredentialsGrantType(client=request.client)

    if request.grant_type == 'authorization_code':
        return AuthorizationCodeGrantType(
            client=request.client,
            auth_code=request.auth_code)

    if request.grant_type == 'password':
        return UserCredentialsGrantType(
            client=request.client,
            user=request.user)

    if request.grant_type == 'refresh_token':
        return RefreshTokenGrantType(
            refresh_token=request.refresh_token)


class ClientRequiredMixin(object):

    def __init__(self, client):
        self.client = client


class CreateTokenMixin(object):

    def create_access_token(self, client, user=None, scope=None):
        refresh_token = OAuthRefreshToken.objects.create(
            refresh_token=unicode(uuid.uuid4()),
            expires_at=OAuthRefreshToken.new_expires_at(),
        )

        return OAuthAccessToken.objects.create(
            access_token=unicode(uuid.uuid4()),
            expires_at=OAuthAccessToken.new_expires_at(),
            client=client,
            user=user,
            scope=scope if scope else settings.OAUTH2_SERVER['DEFAULT_SCOPE'],
            refresh_token=refresh_token,
        )


class ClientCredentialsGrantType(ClientRequiredMixin, CreateTokenMixin):

    def grant(self):
        return self.create_access_token(
            client=self.client)


class UserCredentialsGrantType(ClientRequiredMixin, CreateTokenMixin):

    def __init__(self, client, user):
        super(UserCredentialsGrantType, self).__init__(client=client)
        self.user = user

    def grant(self):
        return self.create_access_token(
            client=self.client, user=self.user)


class AuthorizationCodeGrantType(ClientRequiredMixin, CreateTokenMixin):

    def __init__(self, client, auth_code):
        super(AuthorizationCodeGrantType, self).__init__(client=client)
        self.auth_code = auth_code

    def grant(self):
        if self.auth_code.is_expired():
            self.auth_code.delete()
            raise ExpiredAuthorizationCodeException()

        access_token = self.create_access_token(
            client=self.client, scope=self.auth_code.scope)

        self.auth_code.delete()

        return access_token


class RefreshTokenGrantType(ClientRequiredMixin, CreateTokenMixin):

    def __init__(self, refresh_token):
        self.refresh_token = refresh_token

    def grant(self):
        if self.refresh_token.is_expired():
            self.refresh_token.delete()
            raise ExpiredRefreshTokenException()

        access_token = self.create_access_token(
            client=self.refresh_token.access_token.client,
            user=self.refresh_token.access_token.user)

        self.refresh_token.access_token.delete()
        self.refresh_token.delete()

        return access_token