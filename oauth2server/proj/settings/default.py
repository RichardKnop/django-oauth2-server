# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'rest_framework',
    'apps.credentials',
    'apps.tokens',
    'apps.web',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
)

TIME_ZONE = 'UTC'

ROOT_URLCONF = 'proj.urls'

WSGI_APPLICATION = 'proj.wsgi.application'

ALLOWED_HOSTS = '*'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'proj', 'static'),
)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'proj', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                # 'django.contrib.auth.context_processors.auth',
                # 'django.template.context_processors.debug',
                # 'django.template.context_processors.i18n',
                # 'django.template.context_processors.media',
                'django.template.context_processors.static',
                # 'django.template.context_processors.tz',
                # 'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'EXCEPTION_HANDLER': 'proj.exceptions.custom_exception_handler',
}