from django.db import models

from apps.credentials.models import (
    OAuthClient,
    OAuthUser,
)


class OAuthAccessToken(models.Model):
    token = models.CharField(max_length=40, unique=True)
    expires_at = models.DateField()
    scope = models.CharField(max_length=50, default='')
    client = models.ForeignKey(OAuthClient)
    user = models.ForeignKey(OAuthUser, null=True)

    def __unicode__(self):
        return self.token


class OAuthAuthorizationCode(models.Model):
    code = models.CharField(max_length=40, unique=True)
    expires_at = models.DateField()
    redirect_uri = models.CharField(max_length=200, default='')
    scope = models.CharField(max_length=50, default='')
    client = models.ForeignKey(OAuthClient)
    user = models.ForeignKey(OAuthUser, null=True)

    def __unicode__(self):
        return self.code


class OAuthRefreshTokenToken(models.Model):
    token = models.CharField(max_length=40, unique=True)
    expires_at = models.DateField()
    scope = models.CharField(max_length=50, default='')
    client = models.ForeignKey(OAuthClient)
    user = models.ForeignKey(OAuthUser, null=True)

    def __unicode__(self):
        return self.token