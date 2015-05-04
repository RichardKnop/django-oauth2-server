from django.db import models
from django.conf import settings
from django.utils import timezone

from apps.credentials.models import (
    OAuthClient,
    OAuthUser,
)


class ExpiresMixin(models.Model):
    expires_at = models.DateTimeField()

    class Meta:
        abstract = True

    def is_expired(self):
        return timezone.now() > self.expires_at

    @property
    def expires_in(self):
        now = timezone.now()
        if now >= self.expires_at:
            return 0
        return int(round((self.expires_at - now).total_seconds()))

    @classmethod
    def new_expires_at(cls):
        try:
            lifetime = settings.OAUTH2_SERVER[cls.lifetime_setting]
        except KeyError:
            lifetime = cls.default_lifetime
        return timezone.now() + timezone.timedelta(seconds=lifetime)


class OAuthScope(models.Model):
    """
    See http://tools.ietf.org/html/rfc6749#section-3.3
    """

    scope = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    is_default = models.BooleanField(default=False)

    def __unicode__(self):
        return self.scope


class TokenCodeMixin(models.Model):

    scopes = models.ManyToManyField(OAuthScope)
    client = models.ForeignKey(OAuthClient)
    user = models.ForeignKey(OAuthUser, null=True)

    @property
    def scope(self):
        return ' '.join([s.scope for s in self.scopes.all()])

    class Meta:
        abstract = True


class OAuthRefreshToken(ExpiresMixin):

    refresh_token = models.CharField(max_length=40, unique=True)

    def __unicode__(self):
        return self.token

    lifetime_setting = 'REFRESH_TOKEN_LIFETIME'
    default_lifetime = 1209600  # 14 days


class OAuthAccessToken(TokenCodeMixin, ExpiresMixin):

    access_token = models.CharField(max_length=40, unique=True)
    refresh_token = models.OneToOneField(
        OAuthRefreshToken, null=True, related_name='access_token')

    @property
    def token_type(self):
        return 'Bearer'

    def __unicode__(self):
        return self.token

    lifetime_setting = 'ACCESS_TOKEN_LIFETIME'
    default_lifetime = 3600


class OAuthAuthorizationCode(TokenCodeMixin, ExpiresMixin):

    code = models.CharField(max_length=40, unique=True)
    redirect_uri = models.CharField(max_length=200, null=True)

    def __unicode__(self):
        return self.code

    lifetime_setting = 'AUTH_CODE_LIFETIME'
    default_lifetime = 3600