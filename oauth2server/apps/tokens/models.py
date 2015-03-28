from django.db import models
from django.conf import settings
from django.utils import timezone

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

    @classmethod
    def new_expires_at(cls):
        try:
            code_lifetime = settings.OAUTH2_SERVER[cls.lifetime_setting]
        except KeyError:
            code_lifetime = cls.default_lifetime
        return timezone.now() + timezone.timedelta(seconds=code_lifetime)


class OAuthAccessToken(OauthAbstractToken):

    access_token = models.CharField(max_length=40, unique=True)

    @property
    def token_type(self):
        return 'Bearer'

    def __unicode__(self):
        return self.token

    lifetime_setting = 'ACCESS_TOKEN_LIFETIME'
    default_lifetime = 3600


class OAuthAuthorizationCode(OauthAbstractToken):

    code = models.CharField(max_length=40, unique=True)
    redirect_uri = models.CharField(max_length=200, null=True)

    def __unicode__(self):
        return self.code

    lifetime_setting = 'AUTH_CODE_LIFETIME'
    default_lifetime = 3600


class OAuthRefreshToken(OauthAbstractToken):

    refresh_token = models.CharField(max_length=40, unique=True)

    def __unicode__(self):
        return self.token

    lifetime_setting = 'REFRESH_TOKEN_LIFETIME'
    default_lifetime = 1209600  # 14 days