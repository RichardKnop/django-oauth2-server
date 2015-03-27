# BCrypt was developed to replace md5_crypt for BSD systems.
# It uses a modified version of the Blowfish stream cipher.
# Featuring a large salt and variable number of rounds,
# it's currently the default password hash for many systems
# (notably BSD), and has no known weaknesses.
# See: http://pythonhosted.org/passlib/lib/passlib.hash.bcrypt.html

from passlib.hash import bcrypt

from django.db import models
from django.core.validators import EmailValidator, ValidationError


class OAuthCredentials(models.Model):

    password = models.CharField(max_length=160)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.password = bcrypt.encrypt(self.password)
        elif bcrypt.identify(self.password) is False:
            self.password = bcrypt.encrypt(self.password)
        super(OAuthCredentials, self).save(*args, **kwargs)

    def verify_password(self, raw_password):
        return bcrypt.verify(raw_password, self.password)


class OAuthUser(OAuthCredentials):

    email = models.CharField(
        max_length=254,
        unique=True,
        validators=[EmailValidator()],
    )

    def __unicode__(self):
        return self.email

    def validate_unique(self, exclude=None):
        if self.pk is None:
            queryset = OAuthUser.objects.filter(email__iexact=self.email)
        else:
            queryset = OAuthUser.objects.filter(email__iexact=self.email)\
                .exclude(pk=self.pk)
        if len(queryset) != 0:
            raise ValidationError(u'Email not unique')


class OAuthClient(OAuthCredentials):

    client_id = models.CharField(
        max_length=254,
        unique=True,
        validators=[EmailValidator()],
    )
    redirect_uri = models.CharField(max_length=200, null=True)

    def __unicode__(self):
        return self.identifier