# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Application definition

INSTALLED_APPS = (
    'apps.credentials',
    'apps.tokens',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
)

TIME_ZONE = 'UTC'
