# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Application definition

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'rest_framework',
    'apps.credentials',
    'apps.tokens',
    'apps.web',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    # 'proj.middleware.JSONExceptionMiddleware',
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

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'proj', 'templates'),
)
TEMPLATE_CONTEXT_PROCESSORS = (
    # 'django.contrib.auth.context_processors.auth',
    # 'django.core.context_processors.debug',
    # 'django.core.context_processors.i18n',
    # 'django.core.context_processors.media',
    # 'django.core.context_processors.request',
    'django.core.context_processors.static',
    # 'django.contrib.messages.context_processors.messages',
    # 'django.core.context_processors.request',
)

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

OAUTH2_SERVER = {
    'ACCESS_TOKEN_LIFETIME': 3600,
    'SCOPES': {
        'foo': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
        'bar': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium.',
        'qux': 'Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet.',
    },
}