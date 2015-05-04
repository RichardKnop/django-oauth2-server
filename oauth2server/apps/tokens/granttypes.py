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
        return ClientCredentialsGrantType(
            client=request.client,
            scopes=request.scopes)

    if request.grant_type == 'authorization_code':
        return AuthorizationCodeGrantType(
            client=request.client,
            auth_code=request.auth_code)

    if request.grant_type == 'password':
        return UserCredentialsGrantType(
            client=request.client,
            user=request.user,
            scopes=request.scopes)

    if request.grant_type == 'refresh_token':
        return RefreshTokenGrantType(
            refresh_token=request.refresh_token)


class CreateTokenMixin(object):

    def create_access_token(self, client, user=None):
        refresh_token = OAuthRefreshToken.objects.create(
            refresh_token=unicode(uuid.uuid4()),
            expires_at=OAuthRefreshToken.new_expires_at(),
        )

        access_token = OAuthAccessToken.objects.create(
            access_token=unicode(uuid.uuid4()),
            expires_at=OAuthAccessToken.new_expires_at(),
            client=client,
            user=user,
            refresh_token=refresh_token,
        )
        access_token.scopes.add(*self.scopes)

        return access_token


class ClientCredentialsGrantType(CreateTokenMixin):

    def __init__(self, client, scopes):
        self.client = client
        self.scopes = scopes

    def grant(self):
        return self.create_access_token(
            client=self.client)


class UserCredentialsGrantType(CreateTokenMixin):

    def __init__(self, client, user, scopes):
        self.client = client
        self.user = user
        self.scopes = scopes

    def grant(self):
        return self.create_access_token(
            client=self.client, user=self.user)


class AuthorizationCodeGrantType(CreateTokenMixin):

    def __init__(self, client, auth_code):
        self.client = client
        self.auth_code = auth_code
        self.scopes = self.auth_code.scopes.all()

    def grant(self):
        if self.auth_code.is_expired():
            self.auth_code.delete()
            raise ExpiredAuthorizationCodeException()

        access_token = self.create_access_token(client=self.client)

        self.auth_code.delete()

        return access_token


class RefreshTokenGrantType(CreateTokenMixin):

    def __init__(self, refresh_token):
        self.refresh_token = refresh_token
        self.scopes = self.refresh_token.access_token.scopes.all()

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