from __future__ import absolute_import

from django.conf import settings


try:
    SCOPES = settings.OAUTH2_SERVER['SCOPES']
except KeyError:
    SCOPES = {}

try:
    SCOPE_CHOICES = tuple([
        (k, v) for k, v in settings.OAUTH2_SERVER['SCOPES'].iteritems()
    ])
except KeyError:
    SCOPE_CHOICES = ()