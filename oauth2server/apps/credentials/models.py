# BCrypt was developed to replace md5_crypt for BSD systems.
# It uses a modified version of the Blowfish stream cipher.
# Featuring a large salt and variable number of rounds,
# it's currently the default password hash for many systems
# (notably BSD), and has no known weaknesses.
# See: http://pythonhosted.org/passlib/lib/passlib.hash.bcrypt.html

from django.db import models
from django.core.validators import EmailValidator, ValidationError

from apps.credentials import pwd_context


class OAuthCredentials(models.Model):

    password = models.CharField(max_length=160)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.password = pwd_context.encrypt(secret=self.password)
        elif not pwd_context.identify(hash=self.password):
            self.password = pwd_context.encrypt(secret=self.password)
        super(OAuthCredentials, self).save(*args, **kwargs)

    def verify_password(self, raw_password):
        return pwd_context.verify(secret=raw_password, hash=self.password)


class OAuthUser(OAuthCredentials):
    """
    A user

    >>> # Check that password is converted to a hash upon saving
    >>> user = OAuthUser.objects.create(
    ...     email="foo@example.com",
    ...     password="password",
    ... )
    >>> user.verify_password("password")
    True
    >>> user.verify_password("bogus")
    False
    >>> # Check that password is not hashed again when its value did not change
    >>> user.save()
    >>> user.verify_password("password")
    True
    >>> # Check that password is hashed again when its value changed
    >>> user.password = "$this_is_my_new_password"
    >>> user.save()
    >>> user.verify_password("$this_is_my_new_password")
    True
    >>> # Test email case sensitivity
    >>> OAuthUser(
    ...     email='FoO@example.com',
    ...     password='password',
    ... ).full_clean()
    Traceback (most recent call last):
        ...
    ValidationError: {'__all__': [u'Email not unique']}
    """
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
    """
    A client

    >>> # Check that secret is converted to a hash upon saving
    >>> client = OAuthClient.objects.create(
    ...     client_id="fooclient",
    ...     password="password",
    ... )
    >>> client.verify_password("password")
    True
    >>> client.verify_password("bogus")
    False
    >>> # Check that secret is not hashed again when its value did not change
    >>> client.save()
    >>> client.verify_password("password")
    True
    >>> # Check that secret is hashed again when its value changed
    >>> client.password = "$this_is_my_new_password"
    >>> client.save()
    >>> client.verify_password("$this_is_my_new_password")
    True
    """
    client_id = models.CharField(
        max_length=254,
        unique=True,
        validators=[EmailValidator()],
    )
    redirect_uri = models.CharField(max_length=200, null=True)

    def __unicode__(self):
        return self.client_id