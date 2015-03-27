from django.db import models

from apps.credentials.models import (
    OAuthClient,
    OAuthUser,
)


class OauthAbstractToken(models.Model):

    expires_at = models.DateTimeField()
    scope = models.CharField(max_length=50, null=True)
    client = models.ForeignKey(OAuthClient)
    user = models.ForeignKey(OAuthUser, null=True)

    class Meta:
        abstract = True


class OAuthAccessToken(OauthAbstractToken):

    access_token = models.CharField(max_length=40, unique=True)

    @property
    def token_type(self):
        return 'Bearer'

    def __unicode__(self):
        return self.token


class OAuthAuthorizationCode(OauthAbstractToken):

    code = models.CharField(max_length=40, unique=True)
    redirect_uri = models.CharField(max_length=200, null=True)

    def __unicode__(self):
        return self.code


class OAuthRefreshToken(OauthAbstractToken):

    refresh_token = models.CharField(max_length=40, unique=True)

    def __unicode__(self):
        return self.token