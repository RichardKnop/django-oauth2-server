import sys

from proj.settings.default import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'tbd(pv7679n_w-t++*s_*oon&#v0ubhkxhzvlq51ko2+=dt*z#'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'oauth2server',
        'USER': 'richardknop',
        'PASSWORD': '',
        'HOST': '',
    },
}

if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.sqlite3',
            'NAME':     'test_database.sqlite',
        },
    }

DEBUG = True

OAUTH2_SERVER = {
    'ACCESS_TOKEN_LIFETIME': 3600,
    'AUTH_CODE_LIFETIME': 3600,
    'REFRESH_TOKEN_LIFETIME': 3600,
    'SCOPES': {
        'foo': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
        'bar': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium.',
        'qux': 'Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet.',
    },
}